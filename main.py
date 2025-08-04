import os
import requests
import threading
from flask import Flask

# === Environment Variables from Render Dashboard ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

# === Telegram Messaging Function ===
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=payload)
        return response.json()
    except Exception as e:
        print(f"❌ Telegram error: {str(e)}")
        return None

# === Gold Price Fetch from Finnhub ===
def get_gold_price():
    try:
        url = f"https://finnhub.io/api/v1/quote?symbol=OANDA:XAUUSD&token={FINNHUB_API_KEY}"
        response = requests.get(url)
        data = response.json()

        if 'c' in data:
            current = data['c']
            high = data['h']
            low = data['l']
            return f"🟡 Gold Price (XAUUSD)\nCurrent: ${current}\nHigh: ${high}\nLow: ${low}"
        else:
            return f"❌ Finnhub response error: {data}"
    except Exception as e:
        return f"❌ Error fetching gold price: {str(e)}"

# === Main Bot Logic ===
def run_bot():
    # 1. Notify startup
    send_telegram_message("✅ Gold Signal Bot has started and is running!")

    # 2. Get and send real-time gold price
    gold_price_message = get_gold_price()
    send_telegram_message(gold_price_message)

# === Flask App to Keep Server Alive ===
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Gold Signal Bot is running on Render!"

def start_flask():
    app.run(host='0.0.0.0', port=10000)

# === Entry Point ===
if __name__ == '__main__':
    threading.Thread(target=start_flask).start()
    run_bot()

    print("✅ Debug: Bot is starting")
    print("BOT_TOKEN: [HIDDEN]")
    print("CHAT_ID: [HIDDEN]")
    print("FINNHUB_API_KEY: [HIDDEN]")


    # 1. Notify startup
    send_telegram_message("✅ Gold Signal Bot has started and is running!")

    # 2. Get and send real-time gold price
    gold_price_message = get_gold_price()
    print("📊 Gold price message:", gold_price_message)
    send_telegram_message(gold_price_message)
