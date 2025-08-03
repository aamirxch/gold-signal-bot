import os
import requests
import threading
from flask import Flask
from datetime import datetime
import openai

# === Load environment variables from Render ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# === Set OpenAI API key ===
openai.api_key = OPENAI_API_KEY

# === Flask App to Keep Render Instance Alive ===
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Gold Signal Bot is running on Render!"

def start_flask():
    app.run(host='0.0.0.0', port=10000)

# === Function to Send Telegram Messages ===
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=payload)
        print("✅ Telegram response:", response.json())
    except Exception as e:
        print("❌ Error sending Telegram message:", str(e))

# === Generate Trade Signal with ChatGPT ===
def generate_trade_signal():
    prompt = (
        "Act as a professional gold scalping analyst. Analyze live market conditions and give a clear trade signal for XAUUSD.\n"
        "Use current price action, liquidity zones, RSI, MACD, ADX, volume, EMAs, Bollinger Bands, and Fibonacci levels.\n"
        "Consider high-impact economic news. Give the final summary in this format:\n\n"
        "✅ Final Trade Analysis Summary\n"
        "🟢/🔴/🟡 [Signal Type: BUY / SELL / WAIT] Setup was [Valid and Strong / Weak / Not Confirmed]\n"
        "Entry Zone: ~[Entry Price Range]\n"
        "Exit TP: ✅ [TP Price] or ⏳ Pending\n"
        "Stop Loss (SL): [SL Price or ❌ Not Recommended]\n"
        "Timeframes Checked: [M15, M30, H1, H4, D1]\n"
        "Signal Confidence: [High / Medium / Low]\n"
        "High-Impact News Status: [✅ Clear / ⚠️ Risky]\n"
        "News Effect Summary: [Positive / Negative / Volatile / Uncertain]"
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional trading assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ Error generating signal: {str(e)}"

# === Main Bot Logic ===
def run_bot():
    # 1. Send startup message
    send_telegram_message("✅ Gold Signal Bot has started and is running!")

    # 2. Generate trade signal from ChatGPT
    signal = generate_trade_signal()

    # 3. Send signal to Telegram
    message = f"📡 Gold Signal Bot\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{signal}"
    send_telegram_message(message)

# === Entry Point ===
if __name__ == "__main__":
    # Start Flask in background
    threading.Thread(target=start_flask).start()

    # Start the bot
    run_bot()
