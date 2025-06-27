from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("📱 Submit Account"), KeyboardButton("💰 Balance")],
            [KeyboardButton("💸 Withdraw"), KeyboardButton("👤 Profile")]
        ],
        resize_keyboard=True
    )

def get_cancel_keyboard():
    return ReplyKeyboardMarkup(
        [[KeyboardButton("❌ Cancel")]],
        resize_keyboard=True
    )