**The OTP Receiver Bot is a Telegram bot designed to receive Telegram accounts from users, verify them, and provide monetary compensation. This bot allows users to submit their accounts, manage their balance, and withdraw funds.**

## Features

- **Account Submission**: Users can submit their Telegram accounts with phone numbers
- **Account Verification**: The bot verifies submitted accounts automatically
- **Compensation System**: Users earn money for each verified account
- **Multilingual Support**: Available in 8 languages (English, Spanish, Hindi, Russian, Arabic, French, Portuguese, Turkish)
- **Balance Management**: Users can check their balance and withdraw funds
- **Admin Controls**: Comprehensive admin panel for managing settings and users

## How It Works

1. User submits a phone number through the bot
2. Bot helps the user sign in to the account
3. Account is verified for quality (checks for scam marks, frozen status, spam limitations)
4. If the account meets requirements, the user receives payment
5. Users can withdraw their earnings through various payment methods

## Project Structure

```
bot.py                 # Main bot entry point
config.py              # Configuration settings
lonami.py              # Additional utility client
Receiver/
  force.py             # Force operations
  database/
    database.py        # Database interactions
  handlers/
    admin.py           # Admin command handlers
    help.py            # Help command handlers
    start.py           # Start and language handlers
    utils.py           # Utility functions
    verification.py    # Account verification logic
    withdrawal.py      # Withdrawal process handlers
  utils/
    keyboards.py       # Keyboard layouts
    rm_2fa.py          # 2FA removal utilities
```

## Deployment

### Deploy on StackHost
<div align="left">
  <a href="https://t.me/StackHost">
     <img src="https://graph.org/file/7e91d83f67d20f158cfdc.jpg" alt="Deploy On StackHost" width="150" />
  </a>
</div>

### Deploy on Heroku

You can easily deploy the OTP Receiver Bot to Heroku:

1. Click the button below to deploy:

    [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/yourusername/OTP-Receiver-Bot)

2. Fill in the required environment variables (API_ID, API_HASH, BOT_TOKEN, MONGO_URL, etc.) in the Heroku dashboard.

3. Click **Deploy App**. Heroku will build and start your bot automatically.

4. After deployment, use the Heroku dashboard to manage your app and view logs.

**Note:** Make sure to update the repository URL in the deploy button if you fork or rename the project.

### Manual Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/OTP-Receiver-Bot.git
   cd OTP-Receiver-Bot
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure the bot:
   - Create a Telegram bot using [@BotFather](https://t.me/BotFather) and get the bot token
   - Get your API ID and API HASH from [my.telegram.org](https://my.telegram.org)
   - Set up a MongoDB database
   - Edit the config.py file with your credentials

4. Run the bot:
   ```
   python bot.py
   ```

## Configuration

Edit the config.py file with your own settings:

```python
API_ID = "your_api_id"
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"
MONGO_URL = "your_mongodb_url"
SUDO_USERS = [12345678, 87654321]  # Admin user IDs
LOG_CHANNEL = -1001234567890  # Channel ID for logs
SESSION_CHANNEL = -1001234567890  # Channel ID for sessions
```

### Country Codes Configuration

The `COUNTRY_CODES` dictionary in config.py controls which countries are accepted and their rates:

```python
COUNTRY_CODES = {
    "971": {"name": "United Arab Emirates", "tier": "TIER_2", "flag": "🇦🇪", "rate": 2.5},
    "49": {"name": "Germany", "tier": "TIER_2", "flag": "🇩🇪", "rate": 2.0},
    # Add more countries as needed
}
```

### Payment Methods

Configure available withdrawal methods:

```python
UPI_ID = "your_upi_id"
USDT = "your_usdt_address"
USDT_TRC20 = "your_trc20_address"
USDT_BEP20 = "your_bep20_address"
```

## Admin Commands

- `/admin` - View admin panel
- `/settings` - View and modify bot settings
- `/stats` - Show bot statistics
- users - List registered users
- `/accounts` - List registered accounts
- `/withdrawals` - List withdrawal requests
- `/autoaccept [on/off]` - Enable/disable auto-accept
- `/minwithdraw [amount]` - Set minimum withdrawal amount
- `/setlang [lang]` - Set default language
- `/payment [method] [on/off]` - Enable/disable payment method
- `/country [code] [setting] [value]` - Configure country settings
- `/verify [phone]` - Manually verify an account

## User Commands

- `/start` - Start the bot
- `/help` - Show help message
- `/balance` - Check your balance
- `/profile` - View your profile
- `/withdraw` - Withdraw your funds
- `/language` - Change language
- `/cancel` - Cancel current operation

## Account Verification Process

The bot verifies accounts based on several criteria:
1. Checks if the account is marked as scam
2. Checks if the account is frozen
3. Verifies the spam bot status (can send messages)
4. Attempts to remove 2FA if enabled
5. Rates vary by country based on tier settings

## Withdrawal Process

Users can withdraw their earnings through:
- USDT (BEP20)
- TRX (TRC20)
- UPI (if enabled)

Minimum withdrawal amounts can be set by the admin.

## Disclaimer

This bot is for educational and demonstration purposes only. Ensure you comply with all relevant laws and regulations when using or modifying this bot.

## License

Apache License 2.0[LICENSE]