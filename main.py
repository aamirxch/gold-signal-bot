import os
import openai
import requests
from datetime import datetime

# Load environment variables from Render
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

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
        return f"Error generating signal: {str(e)}"

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": f"📡 Gold Signal Bot\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{message}",
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    signal = generate_trade_signal()
    send_to_telegram(signal)
