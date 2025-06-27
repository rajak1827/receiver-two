from pyrogram import Client, filters
from pyrogram.types import Message
from Receiver.database.database import get_text

@Client.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    """Handle the /help command and help button."""
    user_id = message.from_user.id
    help_text = await get_text(user_id, "help")
    await message.reply_text(help_text)

@Client.on_message(filters.command("support"))
async def support_command(client: Client, message: Message):
    """Handle the /support command."""
 
    support_text = "📞 Need help? Contact our support:\n\n" \
                  "Telegram: @YourSupportUsername\n" \
                  "Email: support@yourdomain.com"
    await message.reply_text(support_text) 