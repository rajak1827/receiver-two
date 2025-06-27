from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL, LANGUAGES
from datetime import datetime

client = AsyncIOMotorClient(MONGO_URL)
db = client['OtpBot']
users_db = db['users']
accounts_db = db['accounts']
withdrawals_db = db['withdrawals']
settings_db = db['settings'] 

async def add_user(user_id: int, language: str = "en"):
    if not await users_db.find_one({"user_id": user_id}):
        await users_db.insert_one({
            "user_id": user_id,
            "language": language,
            "balance": 0.0,
            "verified_accounts": 0,
            "unverified_accounts": 0,
            "created_at": datetime.now()
        })

async def get_user(user_id: int):
    return await users_db.find_one({"user_id": user_id})

async def update_user(user_id: int, update_data: dict):
    return await users_db.update_one(
        {"user_id": user_id},
        {"$set": update_data}
    )

async def add_account(user_id: int, phone: str, session: str, country: str, tier: str = "DEFAULT", 
                      status: str = "pending", twofa_enabled: bool = False, twofa_password: str = None,
                      is_scam: bool = False, is_frozen: bool = False, spam_bot_ok: bool = False, 
                      twofa_removed: bool = False):
    await accounts_db.insert_one({
        "user_id": user_id,
        "phone": phone,
        "session": session,
        "country": country,
        "tier": tier,
        "status": status,
        "submitted_at": datetime.now(),
        "verified_at": None,
        "is_frozen": is_frozen,
        "is_scam": is_scam,
        "twofa_enabled": twofa_enabled,
        "twofa_password": twofa_password,
        "spam_bot_ok": spam_bot_ok,
        "twofa_removed": twofa_removed
    })
    
    
    user = await get_user(user_id)
    new_unverified = user.get("unverified_accounts", 0) + 1
    await update_user(user_id, {"unverified_accounts": new_unverified})

async def update_account(phone: str, update_data: dict):
    if not phone or not isinstance(phone, str) or phone.strip() == "":
        raise ValueError("update_account(): Invalid or missing phone number.")
    return await accounts_db.update_one(
        {"phone": phone},
        {"$set": update_data}
    )


async def get_account(phone: str):
    if not phone:
        return "Phone number cannot be empty."
    return await accounts_db.find_one({"phone": phone})

async def get_user_accounts(user_id: int):
    return await accounts_db.find({"user_id": user_id}).to_list(None)

async def create_withdrawal(user_id: int, method: str, address: str, amount: float):
    withdrawal_id = f"WD-{datetime.now().strftime('%Y%m%d%H%M%S')}-{user_id}"
    await withdrawals_db.insert_one({
        "withdrawal_id": withdrawal_id,
        "user_id": user_id,
        "method": method,
        "address": address,
        "amount": amount,
        "status": "pending",
        "requested_at": datetime.now()
    })
    return withdrawal_id

async def get_withdrawals(user_id: int):
    return await withdrawals_db.find({"user_id": user_id}).to_list(None)

async def update_withdrawal(withdrawal_id: str, update_data: dict):
    return await withdrawals_db.update_one(
        {"withdrawal_id": withdrawal_id},
        {"$set": update_data}
    )

async def get_settings():
    settings = await settings_db.find_one({"_id": "global"})
    if not settings:
        settings = {
            "_id": "global",
            "default_language": "en",
            "min_withdrawal": 5.0,
            "auto_accept": False,
            "withdrawal_methods": {
                "USDT_BEP20": True,
                "TRX_TRC20": True,
                "UPI": False
            },
            "country_settings": {},
            "default_rates": {
                "PREMIUM": 5.0,
                "STANDARD": 3.0,
                "BASIC": 1.0,
                "DEFAULT": 0.5
            }
        }
        await settings_db.insert_one(settings)
    
    
    if isinstance(settings.get("withdrawal_methods"), list):
        settings["withdrawal_methods"] = {
            "USDT_BEP20": True,
            "TRX_TRC20": True,
            "UPI": False
        }
        await update_settings({"withdrawal_methods": settings["withdrawal_methods"]})
    
    return settings

async def update_settings(update_data: dict):
    return await settings_db.update_one(
        {"_id": "global"},
        {"$set": update_data},
        upsert=True
    )

async def get_all_users():
    return await users_db.find().to_list(None)

async def get_all_accounts():
    return await accounts_db.find().to_list(None)

async def get_text(user_id: int, key: str, **kwargs) -> str:
    """Get localized text for a given key based on user's language preference."""
    user = await get_user(user_id)
    settings = await get_settings()
    language = user.get("language", settings["default_language"]) if user else settings["default_language"]
    
    
    text = LANGUAGES.get(language, LANGUAGES["en"]).get(key, LANGUAGES["en"].get(key, f"Missing text: {key}"))
    return text.format(**kwargs) if kwargs else text

async def get_pending_withdrawals():
    return await withdrawals_db.find({"status": "pending"}).to_list(None)

async def get_all_withdrawals():
    return await withdrawals_db.find().to_list(None)

async def get_withdrawal(withdrawal_id: str):
    return await withdrawals_db.find_one({"withdrawal_id": withdrawal_id})