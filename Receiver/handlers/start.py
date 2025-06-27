from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from Receiver.database.database import add_user, get_settings, get_user, update_user
from pyrogram.types import ReplyKeyboardRemove
from config import LANGUAGES, UPDATES_CHANNEL
from .withdrawal import handle_commands
from .help import help_command
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


user_states = {}

@Client.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    settings = await get_settings()
    user = await get_user(user_id)
    
    updates_inline = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📢 Updates", url=f"{UPDATES_CHANNEL}")]
        ]
    )
    
    if not user:
        keyboard = [
            [
                KeyboardButton("🇺🇸 English"),
                KeyboardButton("🇪🇸 Español")
            ],
            [
                KeyboardButton("🇮🇳 हिंदी"),
                KeyboardButton("🇷🇺 Русский")
            ],
            [
                KeyboardButton("🇸🇦 العربية"),
                KeyboardButton("🇫🇷 Français")
            ],
            [
                KeyboardButton("🇧🇷 Português"),
                KeyboardButton("🇹🇷 Türkçe")
            ],
            [KeyboardButton("❌ Cancel")]
        ]
        
        await message.reply_text(
            "🌎 Please select your language:\n"
            "🌍 Por favor, selecciona tu idioma:\n"
            "🌏 कृपया अपनी भाषा चुनें:\n"
            "🌍 Пожалуйста, выберите ваш язык:\n"
            "🌍 الرجاء اختيار لغتك:\n"
            "🌍 Veuillez choisir votre langue:\n"
            "🌍 Por favor, selecione seu idioma:\n"
            "🌍 Lütfen dilinizi seçin:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        await message.reply_text(
            "📢 Stay updated with our latest news!",
            reply_markup=updates_inline
        )
        user_states[user_id] = {"state": "select_language"}
        return
    
    language = user.get("language", settings["default_language"])
    welcome_text = LANGUAGES[language]["welcome"]
    
    keyboard = ReplyKeyboardMarkup(
        [
            [KeyboardButton("📱 Submit Account"), KeyboardButton("💰 Balance")],
            [KeyboardButton("❓ Help"), KeyboardButton("👤 Profile")],
            [KeyboardButton("🌐 Change Language")]
        ],
        resize_keyboard=True
    )
    
    await message.reply_text(welcome_text, reply_markup=keyboard)
    await message.reply_text(
        "📢 Stay updated with our latest news!",
        reply_markup=updates_inline
    )

@Client.on_message(filters.command("language") | filters.regex("^🌐 Change Language$"))
async def language_command(client: Client, message: Message):
    user_id = message.from_user.id
    
    
    keyboard = [
        [
            KeyboardButton("🇺🇸 English"),
            KeyboardButton("🇪🇸 Español")
        ],
        [
            KeyboardButton("🇮🇳 हिंदी"),
            KeyboardButton("🇷🇺 Русский")
        ],
        [
            KeyboardButton("🇸🇦 العربية"),
            KeyboardButton("🇫🇷 Français")
        ],
        [
            KeyboardButton("🇧🇷 Português"),
            KeyboardButton("🇹🇷 Türkçe")
        ],
        [KeyboardButton("❌ Cancel")]
    ]
    
    await message.reply_text(
        "🌎 Please select your language:\n"
        "🌍 Por favor, selecciona tu idioma:\n"
        "🌏 कृपया अपनी भाषा चुनें:\n"
        "🌍 Пожалуйста, выберите ваш язык:\n"
        "🌍 الرجاء اختيار لغتك:\n"
        "🌍 Veuillez choisir votre langue:\n"
        "🌍 Por favor, selecione seu idioma:\n"
        "🌍 Lütfen dilinizi seçin:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    user_states[user_id] = {"state": "select_language"}

@Client.on_message(filters.regex("^(🇺🇸 English|🇪🇸 Español|🇮🇳 हिंदी|🇷🇺 Русский|🇸🇦 العربية|🇫🇷 Français|🇧🇷 Português|🇹🇷 Türkçe|❌ Cancel)$"))
async def handle_language_selection(client: Client, message: Message):
    """Handle language selection."""
    user_id = message.from_user.id
    
    
    if user_id not in user_states or user_states[user_id].get("state") != "select_language":
        return
    
    if message.text == "❌ Cancel":
        user = await get_user(user_id)
        if user:
            
            settings = await get_settings()
            language = user.get("language", settings["default_language"])
            welcome_text = LANGUAGES[language]["welcome"]
            
            keyboard = ReplyKeyboardMarkup(
                [
                    [KeyboardButton("📱 Submit Account"), KeyboardButton("💰 Balance")],
                    [KeyboardButton("❓ Help"), KeyboardButton("👤 Profile")],
                    [KeyboardButton("🌐 Change Language")]
                ],
                resize_keyboard=True
            )
            
            await message.reply_text(welcome_text, reply_markup=keyboard)
        else:
            
            await add_user(user_id, "en")
            
            await update_user(user_id, {
                "balance": 0,
                "verified_accounts": 0,
                "unverified_accounts": 0
            })
            welcome_text = LANGUAGES["en"]["welcome"]
            
            keyboard = ReplyKeyboardMarkup(
                [
                    [KeyboardButton("📱 Submit Account"), KeyboardButton("💰 Balance")],
                    [KeyboardButton("❓ Help"), KeyboardButton("👤 Profile")],
                    [KeyboardButton("🌐 Change Language")]
                ],
                resize_keyboard=True
            )
            
            await message.reply_text("✅ Language set to English")
            await message.reply_text(welcome_text, reply_markup=keyboard)
        
        user_states.pop(user_id, None)
        return
    
    
    lang_map = {
        "🇺🇸 English": "en",
        "🇪🇸 Español": "es",
        "🇮🇳 हिंदी": "hi",
        "🇷🇺 Русский": "ru",
        "🇸🇦 العربية": "ar",
        "🇫🇷 Français": "fr",
        "🇧🇷 Português": "pt",
        "🇹🇷 Türkçe": "tr"
    }
    
    selected_lang = lang_map.get(message.text)
    if not selected_lang:
        await message.reply_text(
            "❌ Invalid language selection!\n"
            "❌ ¡Selección de idioma inválida!\n"
            "❌ अमान्य भाषा चयन!\n"
            "❌ Неверный выбор языка!\n"
            "❌ اختيار لغة غير صالح!\n"
            "❌ Sélection de langue invalide!\n"
            "❌ Seleção de idioma inválida!\n"
            "❌ Geçersiz dil seçimi!",
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton("🌐 Change Language")]], resize_keyboard=True)
        )
        user_states.pop(user_id, None)
        return
    
    
    user = await get_user(user_id)
    if user:
        await update_user(user_id, {"language": selected_lang})
    else:
        
        await add_user(user_id, selected_lang)
        
        await update_user(user_id, {
            "balance": 0,
            "verified_accounts": 0,
            "unverified_accounts": 0
        })
    
    
    welcome_text = LANGUAGES[selected_lang]["welcome"]
    
    
    success_text = {
        "en": "✅ Language set to English",
        "es": "✅ Idioma establecido a Español",
        "hi": "✅ भाषा हिंदी में सेट की गई",
        "ru": "✅ Язык установлен на Русский",
        "ar": "✅ تم تعيين اللغة إلى العربية",
        "fr": "✅ Langue définie sur Français",
        "pt": "✅ Idioma definido para Português",
        "tr": "✅ Dil Türkçe olarak ayarlandı"
    }.get(selected_lang, "✅ Language updated")
    
    keyboard = ReplyKeyboardMarkup(
        [
            [KeyboardButton("📱 Submit Account"), KeyboardButton("💰 Balance")],
            [KeyboardButton("❓ Help"), KeyboardButton("👤 Profile")],
            [KeyboardButton("🌐 Change Language")]
        ],
        resize_keyboard=True
    )
    
    await message.reply_text(success_text)
    await message.reply_text(welcome_text, reply_markup=keyboard)
    user_states.pop(user_id, None)


@Client.on_message(filters.regex("^(💰 Balance|❓ Help|👤 Profile)$"))
async def handle_menu_commands(client: Client, message: Message):
    text = message.text
    command_map = {
        "💰 Balance": "balance",
        "❓ Help": "help",
        "👤 Profile": "profile"
    }
    
    command = command_map.get(text)
    if command == "balance":
        await handle_commands(client, message, command="balance")
    elif command == "help":
        await help_command(client, message)
    elif command == "profile":
        await handle_commands(client, message, command="profile")

@Client.on_message(filters.command("close_keyboard"))
async def close_keyboard(client: Client, message: Message):
    user_id = message.from_user.id
    user = await get_user(user_id)
    settings = await get_settings()
    language = user.get("language", settings["default_language"]) if user else settings["default_language"]
    
    text = {
        "en": "⌨️ Keyboard closed",
        "es": "⌨️ Teclado cerrado",
        "hi": "⌨️ कीबोर्ड बंद कर दिया गया"
    }.get(language, "⌨️ Keyboard closed")
    
    await message.reply_text(text, reply_markup=ReplyKeyboardRemove())