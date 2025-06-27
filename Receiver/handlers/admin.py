from pyrogram import Client, filters
from pyrogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from Receiver.database.database import (
    get_settings, update_settings, withdrawals_db, get_all_users, get_all_accounts, get_account, update_account, get_user, update_user, get_withdrawal, update_withdrawal, get_pending_withdrawals
)
from Receiver.handlers.verification import check_account
from config import SUDO_USERS, COUNTRY_CODES, DEFAULT_RATES, SESSION_CHANNEL, LOG_CHANNEL, CHECKOUT_CHANNEL
import asyncio
import time
from datetime import datetime
import os
from Receiver.utils.rm_2fa import set_2fa_to_01
import json

import logging

logger = logging.getLogger(__name__)

def is_admin(func):
    async def wrapper(client, message):
        user_id = message.from_user.id
        if not user_id in SUDO_USERS:
            await message.reply("You are not authorized to use admin commands.")
            return
        return await func(client, message)
    return wrapper

@Client.on_message(filters.command("admin") & filters.user(SUDO_USERS))
async def admin_panel(client: Client, message: Message):
    help_text = (
        "👨‍💻 Admin Commands:\n\n"
        "/settings - View and manage bot settings\n"
        "/stats - View bot statistics\n"
        "/users - View recent users\n"
        "/accounts - View recent accounts\n"
        "/withdrawals - View recent withdrawals\n"
        "/autoaccept [on/off] - Enable/disable auto-accept\n"
        "/minwithdraw [amount] - Set minimum withdrawal amount\n"
        "/setlang [lang] - Set default language\n"
        "/payment [method] [on/off] - Enable/disable payment method\n"
        "/country - Manage country settings\n"
        "/set_rate - Set rates for countries/tiers\n"
        "/set_tier - Set tier for a country\n"
        "/get_rates - View all rates\n"
        "/reset_rates - Reset rates to default\n"
        "/verify [phone] - Manually verify an account\n"
        "/broadcast [message] - Send message to all users\n"
        "/export - Export all sessions\n"
        "/approve_withdraw [withdrawal_id] - Approve a specific withdrawal\n"
        "/approve_all - Approve all pending withdrawals\n"
        "/change_2fa [phone] [password] - Change 2FA password (defaults to '01')"
    )
    await message.reply_text(help_text)

@Client.on_message(filters.command("settings") & filters.user(SUDO_USERS))
async def settings_command(client: Client, message: Message):
    settings = await get_settings()
    
    
    withdrawal_methods = settings.get("withdrawal_methods", {})
    if not isinstance(withdrawal_methods, dict):
        withdrawal_methods = {
            "USDT_BEP20": True,
            "TRX_TRC20": True,
            "UPI": False
        }
        await update_settings({"withdrawal_methods": withdrawal_methods})
    
    settings_text = (
        "⚙️ Current Settings:\n\n"
        f"🔄 Auto-accept: {'✅ Enabled' if settings.get('auto_accept', False) else '❌ Disabled'}\n"
        f"💰 Min withdrawal: ${settings.get('min_withdrawal', 5.0):.2f}\n"
        f"🌐 Default language: {settings.get('default_language', 'en').upper()}\n\n"
        "💳 Payment Methods:\n"
        f"  • USDT (BEP20): {'✅' if withdrawal_methods.get('USDT_BEP20', True) else '❌'}\n"
        f"  • TRX (TRC20): {'✅' if withdrawal_methods.get('TRX_TRC20', True) else '❌'}\n"
        f"  • UPI: {'✅' if withdrawal_methods.get('UPI', False) else '❌'}\n\n"
        "📝 Settings Commands:\n"
        "/autoaccept [on/off] - Enable/disable auto-accept\n"
        "/minwithdraw [amount] - Set minimum withdrawal amount\n"
        "/setlang [lang] - Set default language\n"
        "/payment [method] [on/off] - Enable/disable payment method"
    )
    await message.reply_text(settings_text)

@Client.on_message(filters.command("stats") & filters.user(SUDO_USERS))
async def stats_command(client: Client, message: Message):
    
    total_users = len(await get_all_users())
    total_accounts = len(await get_all_accounts())
    total_verified = sum(1 for acc in await get_all_accounts() if acc.get('verified', False))
    
    stats_text = (
        "📊 Bot Statistics\n\n"
        f"👥 Total Users: {total_users}\n"
        f"📱 Total Accounts: {total_accounts}\n"
        f"✅ Verified Accounts: {total_verified}\n"
        f"⏳ Pending Accounts: {total_accounts - total_verified}"
    )
    await message.reply_text(stats_text)

@Client.on_message(filters.command("users") & filters.user(SUDO_USERS))
async def users_command(client: Client, message: Message):
    
    users = await get_all_users()
    users_text = "👥 Recent Users:\n\n"
    
    for user in users[-10:]:  
        users_text += f"ID: {user['user_id']}\n"
        users_text += f"Language: {user.get('language', 'en').upper()}\n"
        users_text += f"Balance: ${user.get('balance', 0):.2f}\n"
        users_text += f"Verified: {user.get('verified_accounts', 0)}\n"
        users_text += f"Pending: {user.get('unverified_accounts', 0)}\n"
        users_text += "-------------------\n"
    
    await message.reply_text(users_text)

@Client.on_message(filters.command("accounts") & filters.user(SUDO_USERS))
async def accounts_command(client: Client, message: Message):
    
    accounts = await get_all_accounts()
    accounts_text = "📋 Recent Accounts:\n\n"
    
    for acc in accounts[-10:]:  
        accounts_text += f"Phone: {acc.get('phone', 'Unknown')}\n"
        accounts_text += f"Country: {acc.get('country', 'Unknown')}\n"
        accounts_text += f"Status: {'✅ Verified' if acc.get('verified', False) else '⏳ Pending'}\n"
        accounts_text += f"User ID: {acc.get('user_id', 'Unknown')}\n"
        accounts_text += "-------------------\n"
    
    await message.reply_text(accounts_text)

@Client.on_message(filters.command("withdrawals") & filters.user(SUDO_USERS))
async def withdrawals_command(client: Client, message: Message):
    
    withdrawals = await withdrawals_db.find().sort('timestamp', -1).to_list(10)
    withdrawals_text = "💸 Recent Withdrawals:\n\n"
    
    for w in withdrawals:
        withdrawals_text += f"User ID: {w.get('user_id', 'Unknown')}\n"
        withdrawals_text += f"Amount: ${w.get('amount', 0):.2f}\n"
        withdrawals_text += f"Method: {w.get('method', 'Unknown')}\n"
        withdrawals_text += f"Status: {'✅ Paid' if w.get('paid', False) else '⏳ Pending'}\n"
        withdrawals_text += "-------------------\n"
    
    await message.reply_text(withdrawals_text)


@Client.on_message(filters.command("autoaccept") & filters.user(SUDO_USERS))
async def auto_accept_command(client: Client, message: Message):
    args = message.command
    if len(args) != 2 or args[1] not in ["on", "off"]:
        await message.reply_text("Usage: /autoaccept [on/off]")
        return
    
    new_value = args[1] == "on"
    await update_settings({"auto_accept": new_value})
    await message.reply_text(f"🔄 Auto-accept {'enabled' if new_value else 'disabled'}!")

@Client.on_message(filters.command("minwithdraw") & filters.user(SUDO_USERS))
async def min_withdraw_command(client: Client, message: Message):
    args = message.command
    if len(args) != 2:
        await message.reply_text("Usage: /minwithdraw [amount]")
        return
    
    try:
        amount = float(args[1])
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.reply_text("❌ Please provide a valid positive number!")
        return
    
    await update_settings({"min_withdrawal": amount})
    await message.reply_text(f"💰 Minimum withdrawal amount set to ${amount:.2f}!")

@Client.on_message(filters.command("setlang") & filters.user(SUDO_USERS))
async def set_lang_command(client: Client, message: Message):
    args = message.command
    supported_langs = ["en", "es", "hi", "ru", "ar", "fr", "pt", "tr"]
    
    if len(args) != 2 or args[1] not in supported_langs:
        lang_list = ", ".join(supported_langs)
        await message.reply_text(f"Usage: /setlang [{lang_list}]")
        return
    
    await update_settings({"default_language": args[1]})
    
    
    lang_names = {
        "en": "English",
        "es": "Español",
        "hi": "हिंदी",
        "ru": "Русский",
        "ar": "العربية",
        "fr": "Français",
        "pt": "Português",
        "tr": "Türkçe"
    }
    
    await message.reply_text(f"🌐 Default language set to {lang_names[args[1]]}!")

@Client.on_message(filters.command("payment") & filters.user(SUDO_USERS))
async def payment_method_command(client: Client, message: Message):
    args = message.command
    if len(args) != 3 or args[2] not in ["on", "off"]:
        await message.reply_text(
            "Usage: /payment [method] [on/off]\n"
            "Methods: usdt, trx, upi\n\n"
            "Example: /payment usdt on"
        )
        return
    
    method_map = {
        "usdt": "USDT_BEP20",
        "trx": "TRX_TRC20",
        "upi": "UPI"
    }
    
    method_key = method_map.get(args[1].lower())
    if not method_key:
        await message.reply_text("❌ Invalid method! Use: usdt, trx, or upi")
        return
    
    settings = await get_settings()
    withdrawal_methods = settings.get("withdrawal_methods", {})
    if not isinstance(withdrawal_methods, dict):
        withdrawal_methods = {
            "USDT_BEP20": True,
            "TRX_TRC20": True,
            "UPI": False
        }
    
    withdrawal_methods[method_key] = args[2] == "on"
    await update_settings({"withdrawal_methods": withdrawal_methods})
    
    await message.reply_text(
        f"💳 {method_key.replace('_', ' ')} {'enabled' if args[2] == 'on' else 'disabled'}!"
    )

@Client.on_message(filters.command("country") & filters.user(SUDO_USERS))
async def country_settings_command(client: Client, message: Message):
    args = message.command
    if len(args) < 2:
        await message.reply_text(
            "Usage:\n"
            "/country list - Show all country settings\n"
            "/country enable [country_code] - Enable a country\n"
            "/country disable [country_code] - Disable a country\n"
            "/country rate [country_code] [amount] - Set rate for a country\n"
            "/country capacity [country_code] [limit] - Set max accounts per country\n"
            "/country wait [country_code] [minutes] - Set confirmation wait time"
        )
        return
    
    settings = await get_settings()
    country_settings = settings.get("country_settings", {})
    
    if args[1] == "list":
        
        country_list = []
        for code, info in COUNTRY_CODES.items():
            country_config = country_settings.get(code, {})
            enabled = "✅" if country_config.get("enabled", True) else "❌"
            rate = country_config.get("rate", "Default")
            capacity = country_config.get("capacity", "∞")
            wait_time = country_config.get("wait_time", 2)
            
            country_list.append(
                f"{info['flag']} {info['name']} (+{code}):\n"
                f"   • Status: {enabled}\n"
                f"   • Rate: ${rate}\n"
                f"   • Capacity: {capacity}\n"
                f"   • Wait Time: {wait_time} minutes"
            )
        
        
        chunk_size = 50
        for i in range(0, len(country_list), chunk_size):
            chunk = country_list[i:i + chunk_size]
            with open("country_list.txt", "w", encoding="utf-8") as f:
                f.write("\n\n".join(chunk))
            await message.reply_document(document="country_list.txt", caption=f"Country list exported to country_list.txt ({len(chunk)} countries)")
    
    elif args[1] in ["enable", "disable"] and len(args) == 3:
        country_code = args[2]
        
        if country_code not in COUNTRY_CODES:
            await message.reply_text("❌ Invalid country code!")
            return
        
        enabled = args[1] == "enable"
        
        if country_code not in country_settings:
            country_settings[country_code] = {}
        country_settings[country_code]["enabled"] = enabled
        
        await update_settings({"country_settings": country_settings})
        await message.reply_text(
            f"{COUNTRY_CODES[country_code]['flag']} {COUNTRY_CODES[country_code]['name']} {'enabled' if enabled else 'disabled'}!"
        )

    
    elif args[1] == "capacity" and len(args) == 4:
        country_code = args[2]
        
        try:
            capacity = int(args[3])
        except ValueError:
            await message.reply_text("❌ Invalid capacity number!")
            return
        
        if country_code not in COUNTRY_CODES:
            await message.reply_text("❌ Invalid country code!")
            return
        
        if country_code not in country_settings:
            country_settings[country_code] = {}
        country_settings[country_code]["capacity"] = capacity
        
        await update_settings({"country_settings": country_settings})
        await message.reply_text(
            f"{COUNTRY_CODES[country_code]['flag']} {COUNTRY_CODES[country_code]['name']} capacity set to {capacity}!"
        )
    
    elif args[1] == "wait" and len(args) == 4:
        country_code = args[2]
        
        try:
            wait_time = int(args[3]) * 60  # Convert minutes to seconds
        except ValueError:
            await message.reply_text("❌ Invalid wait time!")
            return
        
        if country_code not in COUNTRY_CODES:
            await message.reply_text("❌ Invalid country code!")
            return
        
        if country_code not in country_settings:
            country_settings[country_code] = {}
        country_settings[country_code]["wait_time"] = wait_time
        
        await update_settings({"country_settings": country_settings})
        await message.reply_text(
            f"{COUNTRY_CODES[country_code]['flag']} {COUNTRY_CODES[country_code]['name']} wait time set to {wait_time // 60} minutes!"
        )
    
    else:
        await message.reply_text("❌ Invalid command format!")


@Client.on_message(filters.command("set_rate") & filters.user(SUDO_USERS))
async def set_rate_command(client: Client, message: Message):
    """Set rate for a specific country or tier
    Usage: /set_rate [country_code/tier] [rate]
    Example: /set_rate 1 5.0 (sets USA/Canada rate to $5.0)
    Example: /set_rate PREMIUM 6.0 (sets PREMIUM tier rate to $6.0)"""
    
    args = message.command[1:]
    if len(args) != 2:
        await message.reply_text(
            "❌ Invalid format!\n\n"
            "Usage:\n"
            "/set_rate [country_code/tier] [rate]\n\n"
            "Examples:\n"
            "/set_rate 1 5.0 (sets USA/Canada rate to $5.0)\n"
            "/set_rate PREMIUM 6.0 (sets PREMIUM tier rate to $6.0)"
        )
        return
    
    target, rate = args
    try:
        rate = float(rate)
        if rate < 0:
            raise ValueError("Rate must be positive")
    except ValueError:
        await message.reply_text("❌ Invalid rate! Please provide a valid positive number.")
        return
    
    settings = await get_settings()
    country_settings = settings.get("country_settings", {})
    
    if target in ["PREMIUM", "STANDARD", "BASIC", "DEFAULT"]:
        
        settings["default_rates"] = settings.get("default_rates", DEFAULT_RATES.copy())
        settings["default_rates"][target] = rate
        await update_settings(settings)
        await message.reply_text(f"✅ {target} tier rate updated to ${rate:.2f}")
    else:
        
        if target not in COUNTRY_CODES:
            await message.reply_text("❌ Invalid country code!")
            return
        
        country_name = COUNTRY_CODES[target]["name"]
        if target not in country_settings:
            country_settings[target] = {}
        country_settings[target]["rate"] = rate
        settings["country_settings"] = country_settings
        await update_settings(settings)
        await message.reply_text(f"✅ Rate for {country_name} updated to ${rate:.2f}")

@Client.on_message(filters.command("set_tier") & filters.user(SUDO_USERS))
async def set_tier_command(client: Client, message: Message):
    """Set tier for a country
    Usage: /set_tier [country_code] [tier]
    Example: /set_tier 91 PREMIUM"""
    
    args = message.command[1:]
    if len(args) != 2:
        await message.reply_text(
            "❌ Invalid format!\n\n"
            "Usage:\n"
            "/set_tier [country_code] [tier]\n\n"
            "Example:\n"
            "/set_tier 91 PREMIUM\n\n"
            "Available tiers: PREMIUM, STANDARD, BASIC, DEFAULT"
        )
        return
    
    country_code, tier = args
    if country_code not in COUNTRY_CODES:
        await message.reply_text("❌ Invalid country code!")
        return
    
    if tier not in ["PREMIUM", "STANDARD", "BASIC", "DEFAULT"]:
        await message.reply_text("❌ Invalid tier! Use: PREMIUM, STANDARD, BASIC, or DEFAULT")
        return
    
    settings = await get_settings()
    country_settings = settings.get("country_settings", {})
    
    country_name = COUNTRY_CODES[country_code]["name"]
    if country_code not in country_settings:
        country_settings[country_code] = {}
    country_settings[country_code]["tier"] = tier
    settings["country_settings"] = country_settings
    await update_settings(settings)
    
    
    tier_rates = settings.get("default_rates", DEFAULT_RATES)
    rate = tier_rates.get(tier, DEFAULT_RATES[tier])
    
    await message.reply_text(
        f"✅ {country_name} moved to {tier} tier\n"
        f"💰 New rate: ${rate:.2f}"
    )

@Client.on_message(filters.command("get_rates") & filters.user(SUDO_USERS))
async def get_rates_command(client: Client, message: Message):
    """View current rates for all countries and tiers"""
    settings = await get_settings()
    tier_rates = settings.get("default_rates", DEFAULT_RATES)
    country_settings = settings.get("country_settings", {})

    response = "📊 Current Rates\n\n"

    response += "🏷 Tier Rates:\n"
    for tier in ["PREMIUM", "STANDARD", "BASIC", "DEFAULT"]:
        rate = tier_rates.get(tier, DEFAULT_RATES[tier])
        response += f"• {tier}: ${rate:.2f}\n"

    response += "\n🌐 Country Rates:\n"
    for code, info in COUNTRY_CODES.items():
        country_name = info["name"]
        flag = info.get("flag", "")
        country_config = country_settings.get(code, {})
        if "rate" in country_config:
            rate = country_config["rate"]
            tier = country_config.get("tier", "Custom")
            response += f"{flag} {country_name} (+{code}): ${rate:.2f} (Custom)\n"
        elif "tier" in country_config:
            tier = country_config["tier"]
            rate = tier_rates.get(tier, DEFAULT_RATES[tier])
            response += f"{flag} {country_name} (+{code}): ${rate:.2f} ({tier})\n"
        else:
            rate = tier_rates.get("DEFAULT", DEFAULT_RATES["DEFAULT"])
            response += f"{flag} {country_name} (+{code}): ${rate:.2f} (Default)\n"

    if len(response) > 4000:
        parts = [response[i:i+4000] for i in range(0, len(response), 4000)]
        for part in parts:
            await message.reply_text(part)
    else:
        await message.reply_text(response)

@Client.on_message(filters.command("reset_rates") & filters.user(SUDO_USERS))
async def reset_rates_command(client: Client, message: Message):
    """Reset all rates to default"""
    settings = await get_settings()
    settings["default_rates"] = DEFAULT_RATES.copy()
    settings["country_settings"] = {}
    await update_settings(settings)
    await message.reply_text("✅ All rates have been reset to default values.")

@Client.on_message(filters.command("broadcast") & filters.user(SUDO_USERS))
async def broadcast_command(client: Client, message: Message):
    """Send a message to all users"""
    
    if len(message.command) < 2:
        await message.reply_text(
            "❌ Please provide a message to broadcast!\n\n"
            "Usage: /broadcast [message]\n"
            "Example: /broadcast 🎉 New feature available!"
        )
        return

    
    broadcast_msg = " ".join(message.command[1:])
    
    
    users = await get_all_users()
    total_users = len(users)
    successful = 0
    failed = 0
    
    
    start_time = time.time()
    
    
    progress_msg = await message.reply_text("📤 Broadcasting message...")
    
    
    for user in users:
        try:
            await client.send_message(
                chat_id=user["user_id"],
                text=broadcast_msg
            )
            successful += 1
            
            
            if successful % 10 == 0:
                try:
                    await progress_msg.edit_text(
                        f"📤 Broadcasting message...\n"
                        f"✅ Sent: {successful}\n"
                        f"❌ Failed: {failed}\n"
                        f"📊 Progress: {((successful + failed) / total_users) * 100:.1f}%"
                    )
                except Exception:
                    pass
                
            
            await asyncio.sleep(0.1)
        except Exception:
            failed += 1
    
    
    await progress_msg.edit_text(
        f"📤 Broadcast completed!\n\n"
        f"📊 Statistics:\n"
        f"👥 Total users: {total_users}\n"
        f"✅ Successfully sent: {successful}\n"
        f"❌ Failed: {failed}\n"
        f"⏱ Time taken: {time.time() - start_time:.1f}s"
    )


@Client.on_message(filters.command("verify") & filters.user(SUDO_USERS))
async def verify_account_command(client: Client, message: Message):
    args = message.command
    print(f"Received command: {args}")

    if len(args) != 2:
        await message.reply_text(
            "Usage: /verify [phone_number]\n"
            "Example: /verify +1234567890"
        )
        return

    phone = args[1]
    print(f"Verifying account for phone: {phone}")

    account = await get_account(phone)
    print(f"Retrieved account: {account}")

    if not account:
        await message.reply_text("❌ Account not found!")
        return

    if account.get("status") == "verified":
        await message.reply_text("⚠️ Account is already verified!")
        return

    status_msg = await message.reply_text("🔄 Verifying account...")

    try:
        settings = await get_settings()
        country_settings = settings["country_settings"].get(account["country"], {})
        
        result = await check_account(phone, client)

        if not result["success"]:
            await update_account(phone, {
                "status": "verification_failed",
                "verification_error": result["error"]
            })
            await status_msg.edit_text(f"❌ Error: {result['error']}")
            return

        # Determine new status
        if result["is_scam"]:
            status = "scam"
        elif result["is_frozen"]:
            status = "frozen"
        elif result["spam_bot_ok"]:
            status = "verified"
        else:
            status = "rejected"

        tier = account.get("tier", "DEFAULT")
        rate = country_settings.get("rate", DEFAULT_RATES[tier])

        await update_account(phone, {
            "status": status,
            "is_frozen": result["is_frozen"],
            "is_scam": result["is_scam"],
            "verified_at": datetime.now(),
            "rate": rate,
            "spam_bot_status": "ok" if result["spam_bot_ok"] else "limited",
            "spam_bot_response": result["spam_bot_response"]
        })

        if status == "verified":
            user = await get_user(account["user_id"])
            new_verified = user.get("verified_accounts", 0) + 1
            new_unverified = max(0, user.get("unverified_accounts", 0) - 1)
            new_balance = user.get("balance", 0) + rate

            await update_user(account["user_id"], {
                "verified_accounts": new_verified,
                "unverified_accounts": new_unverified,
                "balance": new_balance
            })

            await client.send_message(
                account["user_id"],
                f"✅ Account verified successfully!\n"
                f"📱 {phone}\n"
                f"{COUNTRY_CODES[account['country']]['flag']} Country: {account['country']}\n"
                f"💰 Earned: ${rate:.2f}"
            )

            session_file = f"sessions/{account['user_id']}.txt"
            with open(session_file, "w") as f:
                f.write(account["session"])

            await client.send_document(
                SESSION_CHANNEL,
                document=session_file,
                caption=(
                    f"📥 New account submitted!\n"
                    f"👤 User: {account['user_id']}\n"
                    f"📱 Phone: {phone}\n"
                    f"{COUNTRY_CODES[account['country']]['flag']} Country: {account['country']}\n"
                    f"💰 Rate: ${rate:.2f}\n"
                    f"🏷 Status: {status}\n"
                    f"❄️ Frozen: {result['is_frozen']}\n"
                    f"⚠️ Scam: {result['is_scam']}\n"
                    f"🤖 Spam Bot: {'✅ OK' if result['spam_bot_ok'] else '❌ Limited'}\n"
                    f"📝 SpamBot Response: {result['spam_bot_response']}"
                )
            )
        else:
            reason_map = {
                "scam": "Account marked as scam",
                "frozen": "Account is frozen",
                "rejected": "Verification failed" + (
                    " (Spam bot: Limited)" if not result["spam_bot_ok"] else ""
                )
            }

            await client.send_message(
                account["user_id"],
                f"❌ Account rejected!\n"
                f"📱 {phone}\n"
                f"{COUNTRY_CODES[account['country']]['flag']} Country: {account['country']}\n"
                f"❗ Reason: {reason_map.get(status, status)}\n"
                f"📝 SpamBot Response: {result['spam_bot_response']}"
            )

        await client.send_message(
            LOG_CHANNEL,
            f"🔍 Account verification result (Manual)\n"
            f"📱 Phone: {phone}\n"
            f"👤 User: {account['user_id']}\n"
            f"{COUNTRY_CODES[account['country']]['flag']} Country: {account['country']}\n"
            f"💰 Rate: ${rate:.2f}\n"
            f"🏷 Status: {status}\n"
            f"❄️ Frozen: {result['is_frozen']}\n"
            f"⚠️ Scam: {result['is_scam']}\n"
            f"🤖 Spam Bot: {'✅ OK' if result['spam_bot_ok'] else '❌ Limited'}\n"
            f"📝 SpamBot Response: {result['spam_bot_response']}"
        )

        await status_msg.edit_text(
            f"✅ Verification completed!\n\n"
            f"📱 Phone: {phone}\n"
            f"👤 User: {account['user_id']}\n"
            f"{COUNTRY_CODES[account['country']]['flag']} Country: {account['country']}\n"
            f"🏷 Status: {status}\n"
            f"❄️ Frozen: {result['is_frozen']}\n"
            f"⚠️ Scam: {result['is_scam']}\n"
            f"🤖 Spam Bot: {'✅ OK' if result['spam_bot_ok'] else '❌ Limited'}\n"
            f"📝 SpamBot Response: {result['spam_bot_response']}"
        )

    except Exception as e:
        await status_msg.edit_text(f"❌ Error: {str(e)}")


@Client.on_message(filters.command("export") & filters.user(SUDO_USERS))
async def export_sessions_command(client: Client, message: Message):
    accounts = await get_all_accounts()
    sessions = []
    for account in accounts:
        sessions.append(account["phone"] + "\n" + account["session"] + "\n" + str(account["user_id"]))
    with open("sessions.txt", "w") as f:
        for session in sessions:
            f.write(session + "\n\n")
    await message.reply_document(document="sessions.txt", caption=f"Sessions exported to sessions.txt ({len(sessions)} accounts)")


@Client.on_message(filters.command("approve_withdraw") & filters.user(SUDO_USERS))
async def approve_withdraw_command(client: Client, message: Message):
    """Approve a specific withdrawal by ID"""
    try:
        
        args = message.text.split()
        if len(args) != 2:
            await message.reply_text(
                "❌ Please provide the withdrawal ID\n"
                "Usage: /approve_withdraw [withdrawal_id]"
            )
            return
            
        withdrawal_id = args[1]
        
        
        withdrawal = await get_withdrawal(withdrawal_id)
        if not withdrawal:
            await message.reply_text("❌ Withdrawal not found!")
            return
            
        if withdrawal.get("status") == "approved":
            await message.reply_text("❌ This withdrawal is already approved!")
            return
            
        
        await update_withdrawal(withdrawal_id, {"status": "approved"})
        
        
        try:
            await client.send_message(
                withdrawal["user_id"],
                f"✅ Your withdrawal has been approved!\n\n"
                f"💰 Amount: ${withdrawal['amount']:.2f}\n"
                f"💳 Method: {withdrawal['method']}\n"
                f"📝 ID: {withdrawal_id}"
            )
            await client.send_message(
                CHECKOUT_CHANNEL,
                f"✅ Withdrawal approved!\n\n"
                f"👤 User: {withdrawal['user_id']}\n"
                f"💰 Amount: ${withdrawal['amount']:.2f}\n"
                f"💳 Method: {withdrawal['method']}\n"
                f"📝 ID: {withdrawal_id}",
                reply_markup=(
                    InlineKeyboardMarkup([
                        [InlineKeyboardButton("Start", url=f"https://t.me/{(await client.get_me()).username}?start=true")],
                    ])
                )
            )
            await client.send_message(
                LOG_CHANNEL,
                f"✅ Withdrawal approved!\n\n"
                f"👤 User: {withdrawal['user_id']}\n"
                f"💰 Amount: ${withdrawal['amount']:.2f}\n"
                f"💳 Method: {withdrawal['method']}\n"
                f"📝 ID: {withdrawal_id}"
            )

        except Exception as e:
            await message.reply_text(f"⚠️ Could not notify user: {str(e)}")
        
        await message.reply_text(
            f"✅ Withdrawal {withdrawal_id} approved!\n\n"
            f"👤 User: {withdrawal['user_id']}\n"
            f"💰 Amount: ${withdrawal['amount']:.2f}\n"
            f"💳 Method: {withdrawal['method']}\n"
            f"📝 Address: {withdrawal['address']}"
        )
        
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@Client.on_message(filters.command("approve_all") & filters.user(SUDO_USERS))
async def approve_all_command(client: Client, message: Message):
    """Approve all pending withdrawals"""
    try:
        
        pending_withdrawals = await get_pending_withdrawals()
        
        if not pending_withdrawals:
            await message.reply_text("✅ No pending withdrawals found!")
            return
            
        approved_count = 0
        failed_count = 0
        
        for withdrawal in pending_withdrawals:
            try:
                
                await update_withdrawal(withdrawal["_id"], {"status": "approved"})
                
                
                try:
                    await client.send_message(
                        withdrawal["user_id"],
                        f"✅ Your withdrawal has been approved!\n\n"
                        f"💰 Amount: ${withdrawal['amount']:.2f}\n"
                        f"💳 Method: {withdrawal['method']}\n"
                        f"📝 ID: {withdrawal['id']}"
                    )
                    await client.send_message(
                        CHECKOUT_CHANNEL,
                        f"✅ Withdrawal approved!\n\n"
                        f"👤 User: {withdrawal['user_id']}\n"
                        f"💰 Amount: ${withdrawal['amount']:.2f}\n"
                        f"💳 Method: {withdrawal['method']}\n"
                        f"📝 ID: {withdrawal['_id']}",
                        reply_markup=(
                            InlineKeyboardMarkup([
                                [InlineKeyboardButton("Start", url=f"https://t.me/{(await client.get_me()).username}?start=true")],
                            ])
                        )
                    )
                    await client.send_message(
                        LOG_CHANNEL,
                        f"✅ Withdrawal approved!\n\n"
                        f"👤 User: {withdrawal['user_id']}\n"
                        f"💰 Amount: ${withdrawal['amount']:.2f}\n"
                        f"💳 Method: {withdrawal['method']}\n"
                        f"📝 ID: {withdrawal['_id']}"
                    )
                except Exception as e:
                    await message.reply_text(f"⚠️ Could not notify user {withdrawal['user_id']}: {str(e)}")
                
                approved_count += 1
                
            except Exception as e:
                failed_count += 1
                await message.reply_text(
                    f"❌ Failed to approve withdrawal {withdrawal['_id']}: {str(e)}"
                )
        
        await message.reply_text(
            f"✅ Withdrawal approval complete!\n\n"
            f"✅ Successfully approved: {approved_count}\n"
            f"❌ Failed to approve: {failed_count}"
        )
        
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")




@Client.on_message(filters.command("json") & filters.user(SUDO_USERS))
async def replied_message_data(client: Client, message: Message):
    """Get JSON data of the replied message"""
    if not message.reply_to_message:
        await message.reply_text("❌ Please reply to a message to get its JSON data.")
        return
    
    replied_message = message.reply_to_message
    json_data = replied_message.to_dict()
    
    try:
        with open("replied_message.json", "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        
        await message.reply_document(
            document="replied_message.json",
            caption="📄 Replied message JSON data"
        )
    except Exception as e:
        await message.reply_text(f"❌ Error saving JSON data: {str(e)}")