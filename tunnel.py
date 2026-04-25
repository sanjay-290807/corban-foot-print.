#!/usr/bin/env python3
from pyngrok import ngrok
import time

# Start ngrok tunnel
print("🚀 Starting ngrok tunnel...")
tunnel = ngrok.connect(8000, "http")
print(f"✅ Public URL: {tunnel.public_url}")
print("🌐 Your CarbonIQ app is now publicly accessible!")
print("📱 Test it at:", tunnel.public_url)
print("🔄 Tunnel will stay active...")

# Keep the tunnel alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("🛑 Closing tunnel...")
    ngrok.disconnect(tunnel.public_url)
    ngrok.kill()