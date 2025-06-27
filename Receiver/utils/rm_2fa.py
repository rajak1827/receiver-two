import asyncio
from pyrogram import Client
from pyrogram.raw.functions.account import GetPassword
from config import FA_PASSWORD, FA_HINT

async def set_2fa_to_01(client, current_password=None):
    try:
        pw = await client.invoke(GetPassword())

        if pw.has_password:
            if not current_password:
                return "Enter your 2FA password to submit the request."
            if pw.has_recovery:
                return "You have recovery codes set up. Please disable them before changing your 2FA password."
            try:
                await client.change_cloud_password(
                    current_password=current_password,
                    new_password=f"{FA_PASSWORD}",
                    new_hint=f"{FA_HINT}"
                )
                print("✅ 2FA password changed to '01'")
                return True
            except Exception as e:
                print(f"❌ Failed to change 2FA password: {e}")
                return False
        else:
            # 2FA not set, enable it with '01'
            try:
                await client.enable_cloud_password(
                    password=f"{FA_PASSWORD}",
                    hint=f"{FA_HINT}",
                )
                print("✅ 2FA password enabled with '01'")
                return True
            except Exception as e:
                print(f"❌ Failed to enable 2FA password: {e}")
                return False

    except ValueError as e:
        print(f"❌ Invalid password: {e}")
        return False
    except asyncio.TimeoutError:
        print("❌ Request timed out while fetching password settings.")
        return False
    except Exception as e:
        print(f"❌ Error fetching password settings: {e}")
        return False
