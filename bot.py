from config import API_ID, API_HASH, BOT_TOKEN
import logging
from pyrogram import Client, idle, compose
from pyromod import listen  
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid
from lonami import lonami
import asyncio

user_states = {}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(pathname)s: %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)


app = Client(
    "ohh",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True,
    plugins={'root':'Receiver'},
)

async def main():
    """Main function to run both clients simultaneously"""
    try:
        
        clients = [app, lonami]
        await compose(clients)
    except (ApiIdInvalid, ApiIdPublishedFlood):
        logging.error("Your API_ID/API_HASH is not valid.")
        raise Exception("Your API_ID/API_HASH is not valid.")
    except AccessTokenInvalid:
        logging.error("Your BOT_TOKEN is not valid.")
        raise Exception("Your BOT_TOKEN is not valid.")
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise
    finally:
        
        logging.info("Stopping clients...")
        try:
            await app.stop()
        except Exception as e:
            logging.error(f"Error stopping main app: {e}")
        
        try:
            await lonami.stop()
        except Exception as e:
            logging.error(f"Error stopping lonami client: {e}")
        
        logging.info("Bot stopped")

if __name__ == "__main__":
    logging.info("Starting the bot")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    except Exception as e:
        logging.error(f"Error in main loop: {e}")
    finally:
        loop.close()