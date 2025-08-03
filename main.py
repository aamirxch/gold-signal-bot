import os
import openai
import requests
import threading
from datetime import datetime
from flask import Flask

# === Load Environment Variables from Render ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# === Configure OpenAI ===
openai.api_key = OPENAI_API_KEY

# === Generate Gold Trade Signal ===
def generate_trade_signal():
    prompt = (
        "You are a professional gold scalping analyst. Analyze live market conditions for XAUUSD.\n"
        "Use multi-timeframe analysis (M15, M30, H1, H4, D1), liquidity zones, RSI(14), MACD, ADX, EMAs, Bollinger Bands, Volume, Fibonacci, Fractals, and Fair Value Gaps.\n"
        "Consider high-impact economic news. Return final summary only using this format:\n\n"
        "✅ Final Trade Analysis Summary\n"
        "🔴/🟢/🟡 [SELL / BUY / WAIT] Setup was [Valid and Strong / Weak / Not Confirmed]\n"
        "Entry Zone: ~[Entry Price Range]\n"
        "Exit TP: ✅ [TP Price] or ⏳ Pending\n"
        "Stop Loss (SL): [SL Price or ❌ Not Recommended]\n"
        "Timeframes Checked: [M15, M30, H1, H4, D1]\n"
        "Signal Confidence: [High / Medium / Low]\n"
        "High-Impact News Status: [✅ Clear / ⚠️ Risky]\n"
        "News Effect Summary: [Positive / Negative / Volatile / Uncertain]\n\n"
        "🧠 Only give Entry, TP, and SL if no high-impact news is near.\n"
        "If news is near, advise to WAIT, and reassess after release.\n"
        "💡 Highlight reasons clearly using price action, indicator alignment, volume, and structure."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional gold trading assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Error generating signal: {str(e)}"

# === Send Signal to Telegram ===
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": f"📡 *Gold Signal Bot*\n_{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n\n{message}",
        "parse_mode": "Markdown"
    }
    try:
        res = requests.post(url, json=payload)
        if not res.ok:
            print(f"❌ Telegram Error: {res.text}")
    except Exception as e:
        print(f"❌ Telegram Exception: {str(e)}")

# === Flask Server to Keep Alive on Render ===
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Gold Signal Bot is running on Render!"

def start_flask():
    app.run(host='0.0.0.0', port=10000)

# === Main Function ===
def run_bot():
    signal = generate_trade_signal()
    send_to_telegram(signal)

# === Run Flask + Bot ===
if __name__ == '__main__':
    threading.Thread(target=start_flask).start()
    run_bot()
