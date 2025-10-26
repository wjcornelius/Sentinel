# config.example.py
#
# This is a TEMPLATE configuration file for Sentinel.
# Copy this file to 'config.py' and fill in your actual API keys.
#
# IMPORTANT: Never commit config.py to version control!
# The .gitignore file ensures config.py is excluded from git.

# --- Master switch for live trading ---
# Set to True to execute real paper trades with Alpaca.
# Set to False to run in "SAFE MODE" (simulates trades in the console).
LIVE_TRADING = False  # Start in safe mode by default

# Allow multiple runs per day (useful for development/testing)
# Set to False in production to prevent accidental duplicate trading
ALLOW_DEV_RERUNS = False

# --- Alpaca API Keys (Paper Trading) ---
# Get your API keys from: https://app.alpaca.markets/paper/dashboard/overview
APCA_API_KEY_ID = "YOUR_ALPACA_KEY_ID_HERE"
APCA_API_SECRET_KEY = "YOUR_ALPACA_SECRET_KEY_HERE"
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"

# Specify the data feed to use
# "iex" = free tier (15-minute delayed)
# "sip" = paid tier (real-time data)
APCA_API_DATA_FEED = "iex"

# --- Twilio API Keys (Optional - for SMS notifications) ---
# Get your keys from: https://www.twilio.com/console
TWILIO_ACCOUNT_SID = "YOUR_TWILIO_ACCOUNT_SID_HERE"
TWILIO_AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN_HERE"
TWILIO_PHONE_NUMBER = "YOUR_TWILIO_PHONE_NUMBER_HERE"
RECIPIENT_PHONE_NUMBER = "YOUR_RECIPIENT_PHONE_NUMBER_HERE"

# --- OpenAI API Key ---
# Get your API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY_HERE"

# --- Perplexity API Key ---
# Get your API key from: https://www.perplexity.ai/settings/api
PERPLEXITY_API_KEY = "YOUR_PERPLEXITY_API_KEY_HERE"
