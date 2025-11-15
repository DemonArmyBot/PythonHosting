# app.py
import asyncio
import threading
import time
import requests
import os
from main import main as run_bot_main  # <-- YEH IMPORT HAI!

RENDER_URL = os.environ.get('RENDER_EXTERNAL_URL')
PING_INTERVAL = 300

def pinger():
    while True:
        time.sleep(PING_INTERVAL)
        if RENDER_URL:
            try:
                requests.get(RENDER_URL, timeout=10)
                print(f"Pinged {RENDER_URL}")
            except:
                pass

def run_async_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(run_bot_main())
    except Exception as e:
        print(f"Bot error: {e}")
        time.sleep(10)
        run_async_bot()

from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running! Check /health"

@app.route('/health')
def health():
    return {"status": "alive"}

# Start background
def start_all():
    threading.Thread(target=pinger, daemon=True).start()
    threading.Thread(target=run_async_bot, daemon=True).start()

if __name__ == '__main__':
    start_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, use_reloader=False)