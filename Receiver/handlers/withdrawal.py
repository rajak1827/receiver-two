import random
import string
from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from Receiver.database.database import get_user, create_withdrawal, update_user, get_settings, get_text
from config import LOG_CHANNEL, CHECKOUT_CHANNEL
from pyrogram.types import ReplyKeyboardRemove
import asyncio

@Client.on_message(filters.command(["withdraw", "balance", "profile"]))
async def handle_commands(client: Client, message: Message, command: str = None):
    """Handle balance, profile, and withdrawal commands."""
    if not command:
        command = message.text.split()[0][1:] if message.text.startswith('/') else None
    
    if not command:
        return
        
    user_id = message.from_user.id
    user = await get_user(user_id)
    settings = await get_settings()
    
    if not user:
        await message.reply_text("❌ User not found!")
        return
    
    language = user.get("language", "en")
    
    if command == "balance":
        balance_text = await get_text(user_id, "balance", balance=user['balance'])
        await message.reply_text(balance_text)
    
    elif command == "profile":
        profile_text = await get_text(
            user_id, 
            "profile",
            verified_accounts=user['verified_accounts'],
            unverified_accounts=user['unverified_accounts'],
            balance=user['balance'],
            language=user.get('language', 'en').upper()
        )
        await message.reply_text(profile_text)
    
    elif command == "withdraw":
        min_withdrawal = settings.get("min_withdrawal", 10.0)
        balance = user.get("balance", 0)
        
        if balance < min_withdrawal:
            insufficient_text = await get_text(user_id, "insufficient_withdrawal", min_withdrawal=min_withdrawal, balance=balance)
            await message.reply_text(insufficient_text, reply_markup=ReplyKeyboardRemove())
            return
        
        
        methods = []
        withdrawal_methods = settings.get("withdrawal_methods", {})
        
        if withdrawal_methods.get("USDT_BEP20"):
            methods.append(KeyboardButton("USDT (BEP20)"))
        if withdrawal_methods.get("TRX_TRC20"):
            methods.append(KeyboardButton("TRX (TRC20)"))
        if withdrawal_methods.get("UPI"):
            methods.append(KeyboardButton("UPI"))
        
        if not methods:
            await message.reply_text("❌ No withdrawal methods available!")
            return
        
        select_method_text = await get_text(user_id, "select_withdrawal_method")
        select_method_text += "\n\nUse /cancel to cancel the operation."
        
        await message.reply_text(
            select_method_text,
            reply_markup=ReplyKeyboardMarkup([methods], resize_keyboard=True)
        )
        await handle_withdrawal_process(client, message, user)

async def handle_withdrawal_process(client: Client, message: Message, user: dict):
    user_id = message.from_user.id
    settings = await get_settings()
    min_withdrawal = settings.get("min_withdrawal", 10.0)
    language = user.get("language", "en")
    
    try:
        
        method_msg = await client.listen(user_id, timeout=300)  
        text = method_msg.text
        
        cancel_text = await get_text(user_id, "withdrawal_cancelled")
        
        if text == "/cancel":
            await method_msg.reply_text(cancel_text, reply_markup=ReplyKeyboardRemove())
            return
        
        if text not in ["USDT (BEP20)", "TRX (TRC20)", "UPI"]:
            invalid_method_text = await get_text(user_id, "invalid_method_selected")
            
            await method_msg.reply_text(invalid_method_text, reply_markup=ReplyKeyboardRemove())
            return
        
        method_map = {
            "USDT (BEP20)": "USDT_BEP20",
            "TRX (TRC20)": "TRX_TRC20",
            "UPI": "UPI"
        }
        method_key = method_map[text]
        
        
        address_text = await get_text(user_id, "enter_address", method=text)
        address_text += "\n\nUse /cancel to cancel the operation."
        
        await method_msg.reply_text(
            address_text,
            reply_markup=ReplyKeyboardRemove()
        )
        
        
        address_msg = await client.listen(user_id, timeout=300)  
        address = address_msg.text
        
        if address == "/cancel":
            await address_msg.reply_text(cancel_text, reply_markup=ReplyKeyboardRemove())
            return
        
        
        amount_text = await get_text(user_id, "enter_amount", min_withdrawal=min_withdrawal)
        amount_text += "\n\nUse /cancel to cancel the operation."
        
        await address_msg.reply_text(
            amount_text,
            reply_markup=ReplyKeyboardRemove()
        )
        
        
        amount_msg = await client.listen(user_id, timeout=300)  
        amount_text = amount_msg.text
        
        if amount_text == "/cancel":
            await amount_msg.reply_text(cancel_text, reply_markup=ReplyKeyboardRemove())
            return
        
        try:
            amount = float(amount_text)
            if amount < min_withdrawal:
                error_text = await get_text(user_id, "withdrawal_error", min_withdrawal=min_withdrawal, amount=amount)
                await amount_msg.reply_text(error_text, reply_markup=ReplyKeyboardRemove())
                return
            
            if amount > user.get("balance", 0):
                insufficient_text = await get_text(user_id, "insufficient_balance", balance=user['balance'])
                await amount_msg.reply_text(insufficient_text, reply_markup=ReplyKeyboardRemove())
                return
            
            
            withdrawal_id = await create_withdrawal(
                user_id,
                method_key,
                address,
                amount
            )
            
            
            new_balance = user.get("balance", 0) - amount
            await update_user(user_id, {"balance": new_balance})
            
            
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            
            success_text = await get_text(
                user_id, 
                "withdrawal_submitted", 
                amount=amount,
                withdrawal_id=withdrawal_id, 
                code=code
            )
            
            await amount_msg.reply_text(success_text, reply_markup=ReplyKeyboardRemove())
            
            
            await client.send_message(
                LOG_CHANNEL,
                f"💸 New withdrawal request!\n"
                f"👤 User: {user_id}\n"
                f"💰 Amount: ${amount:.2f}\n"
                f"💳 Method: {text}\n"
                f"📝 ID: {withdrawal_id}\n"
                f"🔑 Code: {code}\n"
                f"Wallet: {address}"
            )
            
        except ValueError:
            error_text = await get_text(user_id, "withdrawal_error", min_withdrawal=min_withdrawal, amount=amount_text)
            await amount_msg.reply_text(error_text, reply_markup=ReplyKeyboardRemove())
            return
            
    except asyncio.TimeoutError:
        timeout_text = await get_text(user_id, "withdrawal_timeout")
        await message.reply_text(timeout_text, reply_markup=ReplyKeyboardRemove())
    except Exception as e:
        error_text = await get_text(user_id, "withdrawal_error")
        await message.reply_text(f"{error_text}: {str(e)}", reply_markup=ReplyKeyboardRemove())