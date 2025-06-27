import asyncio
import re
import zipfile
import os
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.raw import functions

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)


if not os.path.exists("sessions"):
    os.makedirs("sessions")

API_ID = 25667269
API_HASH = "9941534ef2a1b5466e157baf26f29db2"
BOT_TOKEN = "8171246598:AAFn1GBxQcam6H_DLu48WlgWgfZ6IL8_3BQ"


user_sessions = {}

lonami = Client(
    "session_converter",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@lonami.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "👋 Hello! I can convert session files to OTP codes.\n\n"
        "📝 Usage: Send me a session.txt file or a zip file containing multiple sessions and reply to it with /otp"
    )

@lonami.on_message(filters.command("otp") & filters.private)
async def otp(client, message):
    if not message.reply_to_message:
        await message.reply_text("❌ Please reply to a session.txt file or a zip file!")
        return
    
    if not message.reply_to_message.document:
        await message.reply_text("❌ Please send a valid session.txt or zip file!")
        return
    
    document = message.reply_to_message.document
    status_msg = await message.reply_text("🔄 Processing your file...")
    
    try:
        file_path = f"sessions/temp_{message.from_user.id}{os.path.splitext(document.file_name)[1]}"
        await message.reply_to_message.download(file_path)
        
        sessions_list = []
        
        if document.file_name.endswith('.zip'):
            await status_msg.edit_text("🔄 Processing zip file...")
            extract_dir = f"sessions/extract_{message.from_user.id}"
            os.makedirs(extract_dir, exist_ok=True)
            
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            
            for root, dirs, files in os.walk(extract_dir):
                for file in files:
                    if file.endswith('.txt'):
                        session_path = os.path.join(root, file)
                        with open(session_path, "r") as f:
                            session_string = f.read().strip()
                            sessions_list.append(session_string)
            
            
            try:
                os.remove(file_path)
            except:
                pass
        
        elif document.file_name.endswith('.txt'):
            with open(file_path, "r") as f:
                session_string = f.read().strip()
                sessions_list.append(session_string)
            
            
            try:
                os.remove(file_path)
            except:
                pass
        
        else:
            await status_msg.edit_text("❌ Invalid file format! Please send a .txt or .zip file.")
            return
        
        if not sessions_list:
            await status_msg.edit_text("❌ No valid session files found!")
            return
        
        
        user_sessions[message.from_user.id] = {
            "sessions": sessions_list,
            "current_index": 0
        }
        
        await status_msg.edit_text(
            f"✅ Loaded {len(sessions_list)} sessions!\n\nClick Start to begin fetching OTPs",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Start", callback_data="start_otp_fetch")]
            ])
        )
        
    except Exception as e:
        await status_msg.edit_text(f"❌ Error processing file: {str(e)}")

@lonami.on_callback_query(filters.regex(r"start_otp_fetch"))
async def start_otp_fetch(client, callback_query):
    user_id = callback_query.from_user.id
    
    if user_id not in user_sessions or not user_sessions[user_id]["sessions"]:
        await callback_query.answer("No sessions available", show_alert=True)
        await callback_query.message.edit_text("❌ No sessions available")
        return
    
    user_data = user_sessions[user_id]
    current_index = user_data["current_index"]
    
    if current_index >= len(user_data["sessions"]):
        await callback_query.answer("All sessions processed", show_alert=True)
        await callback_query.message.edit_text("✅ All sessions processed")
        return
    
    session_string = user_data["sessions"][current_index]
    
    await callback_query.answer()
    status_msg = callback_query.message
    
    await status_msg.edit_text("🔄 Processing session...")
    
    try:
        temp_client = Client(
            f"user_{user_id}_{current_index}",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=session_string,
            in_memory=True
        )
        
        try:
            await temp_client.start()
            me = await temp_client.get_me()
            phone_number = me.phone_number if me.phone_number else "Unknown"
            
            await status_msg.edit_text(
                f"User: {me.first_name or 'Unknown'}\n"
                f"Number: +{phone_number}\n"
                f"Session {current_index + 1}/{len(user_data['sessions'])}\n\n"
                f"Please check if you have requested OTP",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Check OTP", callback_data="check_otp")]
                ])
            )
            
            
            user_sessions[user_id]["current_client"] = temp_client
            
        except Exception as e:
            await status_msg.edit_text(
                f"❌ Error with session {current_index + 1}: {str(e)}\n\n"
                f"Moving to next session...",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Next Session", callback_data="next_session")]
                ])
            )
            await temp_client.stop()
    
    except Exception as e:
        await status_msg.edit_text(
            f"❌ Error processing session {current_index + 1}: {str(e)}\n\n"
            f"Moving to next session...",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Next Session", callback_data="next_session")]
            ])
        )

@lonami.on_callback_query(filters.regex(r"check_otp"))
async def check_otp(client, callback_query):
    user_id = callback_query.from_user.id
    
    if user_id not in user_sessions or "current_client" not in user_sessions[user_id]:
        await callback_query.answer("Session not available", show_alert=True)
        return
    
    await callback_query.answer()
    status_msg = callback_query.message
    await status_msg.edit_text(f"{status_msg.text}\n\n🔄 Checking for OTP and 2FA...")
    
    user_data = user_sessions[user_id]
    temp_client = user_data["current_client"]
    current_index = user_data["current_index"]
    
    try:
        otp_found = False
        twofa_info = None
        otp = None
        
        
        try:
            
            
            cloud_password = await temp_client.invoke(
                functions.account.GetPassword()
            )
            
            if cloud_password and hasattr(cloud_password, "has_password") and cloud_password.has_password:
                hint = cloud_password.hint if hasattr(cloud_password, "hint") else "No hint available"
                email = cloud_password.email_unconfirmed_pattern if hasattr(cloud_password, "email_unconfirmed_pattern") else "No email available"
                
                twofa_info = {
                    "hint": hint,
                    "email": email,
                    "has_recovery": hasattr(cloud_password, "has_recovery") and cloud_password.has_recovery
                }
        except Exception as e:
            logging.error(f"Error getting 2FA info: {str(e)}")
        
        
        async for msg in temp_client.get_chat_history(777000, limit=5):
            if "Login code:" in msg.text:
                match = re.search(r'Login code: (\d+)', msg.text)
                if match:
                    otp = match.group(1)
                    otp_found = True
                    break
        
        
        base_text = status_msg.text.split('🔄')[0]
        result_text = base_text
        
        if otp_found:
            result_text += f"\n✅ Found OTP: `{otp}`"
        
        if twofa_info:
            result_text += f"\n🔐 2FA Password Info:"
            result_text += f"\n   - Hint: `{twofa_info['hint']}`"
            result_text += f"\n   - Recovery Email: `{twofa_info['email']}`"
            result_text += f"\n   - Has Recovery: `{twofa_info['has_recovery']}`"
        
        if otp_found or twofa_info:
            await status_msg.edit_text(
                result_text,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Next Session", callback_data="next_session")]
                ])
            )
        else:
            await status_msg.edit_text(
                f"{base_text}\n"
                f"❌ No recent OTP found!\n"
                f"❌ No 2FA information available\n\n"
                f"This could mean:\n"
                f"1. No recent login attempts\n"
                f"2. Session is too old\n"
                f"3. Session is invalid",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Check Again", callback_data="check_otp")],
                    [InlineKeyboardButton("Next Session", callback_data="next_session")]
                ])
            )
    
    except Exception as e:
        await status_msg.edit_text(
            f"{status_msg.text.split('🔄')[0]}\n"
            f"❌ Error checking OTP/2FA: {str(e)}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Next Session", callback_data="next_session")]
            ])
        )

@lonami.on_callback_query(filters.regex(r"next_session"))
async def next_session(client, callback_query):
    user_id = callback_query.from_user.id
    
    if user_id not in user_sessions:
        await callback_query.answer("No sessions available", show_alert=True)
        return
    
    user_data = user_sessions[user_id]
    
    
    if "current_client" in user_data:
        try:
            await user_data["current_client"].stop()
        except:
            pass
        del user_data["current_client"]
    
    
    user_data["current_index"] += 1
    current_index = user_data["current_index"]
    
    
    if current_index >= len(user_data["sessions"]):
        await callback_query.answer("All sessions processed", show_alert=True)
        await callback_query.message.edit_text("✅ All sessions processed")
        return
    
    
    await callback_query.answer()
    await start_otp_fetch(client, callback_query)


 
  