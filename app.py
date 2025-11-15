# app.py
import asyncio
import threading
import time
import requests
import os
from main import main as run_bot_main

# Render URL
RENDER_URL = os.environ.get('RENDER_EXTERNAL_URL')
PING_INTERVAL = 300  # 5 minutes

# Pinger (background thread mein chalega)
def pinger():
    while True:
        time.sleep(PING_INTERVAL)
        if RENDER_URL:
            try:
                requests.get(RENDER_URL, timeout=10)
                print(f"Pinged {RENDER_URL}")
            except:
                print("Ping failed")
        else:
            print("RENDER_URL not set yet...")

# Flask app (background mein chalega)
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive! Aiogram running in main thread."

@app.route('/health')
def health():
    return {"status": "ok", "bot": "main thread"}

# Run Flask in background thread
def run_flask():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, use_reloader=False)

# Main entry point
if __name__ == '__main__':
    # Start Flask in background
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Start pinger
    threading.Thread(target=pinger, daemon=True).start()

    print("Starting bot in MAIN THREAD...")

    # Run bot in MAIN THREAD (asyncio allowed here)
    try:
        asyncio.run(run_bot_main())
    except Exception as e:
        print(f"Bot crashed: {e}")