from pyrogram import Client
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

async def cancel_command(client: Client, message: Message):
    """Cancel the current operation and return to main menu"""
    keyboard = ReplyKeyboardMarkup(
        [
            [KeyboardButton("📱 Submit Account"), KeyboardButton("💰 Balance")],
            [KeyboardButton("❓ Help"), KeyboardButton("👤 Profile")],
            [KeyboardButton("🌐 Change Language")]
        ],
        resize_keyboard=True
    )
    
    await message.reply_text(
        "❌ Operation cancelled. Back to main menu.",
        reply_markup=keyboard
    )