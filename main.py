import os
import asyncio
import time
from datetime import datetime

# Minimalny selfbot bez discord.py
import aiohttp
import json

class SimpleSelfBot:
    def __init__(self):
        self.token = os.getenv('DISCORD_TOKEN')
        self.channel1_id = os.getenv('SERVER1_CHANNEL_ID')
        self.channel2_id = os.getenv('SERVER2_CHANNEL_ID')
        self.interval1 = int(os.getenv('INTERVAL_SECONDS_1', 300))
        self.interval2 = int(os.getenv('INTERVAL_SECONDS_2', 300))
        
        self.session = None
        self.counter1 = 1
        self.counter2 = 1
        
    async def send_message(self, channel_id, content):
        if not self.session:
            self.session = aiohttp.ClientSession(headers={
                'Authorization': self.token,
                'Content-Type': 'application/json'
            })
            
        url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
        data = {'content': content}
        
        try:
            async with self.session.post(url, json=data) as response:
                if response.status == 200:
                    print(f"✅ Wiadomość wysłana na kanał {channel_id}")
                else:
                    text = await response.text()
                    print(f"❌ Błąd {response.status}: {text}")
        except Exception as e:
            print(f"❌ Błąd wysyłania: {e}")
    
    async def run(self):
        print("🟡 Uruchamianie selfbota...")
        
        while True:
            try:
                # Serwer 1
                if self.channel1_id:
                    await self.send_message(
                        self.channel1_id, 
                        f"Auto wiadomość #{self.counter1} | Serwer 1 | {datetime.now().strftime('%H:%M:%S')}"
                    )
                    self.counter1 += 1
                    await asyncio.sleep(self.interval1)
                
                # Serwer 2
                if self.channel2_id:
                    await self.send_message(
                        self.channel2_id,
                        f"Auto wiadomość #{self.counter2} | Serwer 2 | {datetime.now().strftime('%H:%M:%S')}"
                    )
                    self.counter2 += 1
                    await asyncio.sleep(self.interval2)
                    
            except Exception as e:
                print(f"❌ Błąd: {e}")
                await asyncio.sleep(60)

if __name__ == "__main__":
    bot = SimpleSelfBot()
    asyncio.run(bot.run())
