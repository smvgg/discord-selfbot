import os
import asyncio
import time
from datetime import datetime
from aiohttp import web
import aiohttp
import json

# Dodaj prosty serwer HTTP dla portu
async def health_check(request):
    return web.Response(text="Bot is running")

app = web.Application()
app.router.add_get('/', health_check)

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
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
            })
            
        url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
        data = {'content': content}
        
        try:
            print(f"📤 Próba wysłania: {content}")
            async with self.session.post(url, json=data) as response:
                if response.status == 200:
                    print(f"✅ Wiadomość wysłana na kanał {channel_id}")
                    return True
                else:
                    text = await response.text()
                    print(f"❌ Błąd {response.status}: {text}")
                    return False
        except Exception as e:
            print(f"❌ Błąd wysyłania: {e}")
            return False
    
    async def run_bot(self):
        print("🟡 Uruchamianie selfbota...")
        print(f"📝 Kanał 1: {self.channel1_id}, interwał: {self.interval1}s")
        print(f"📝 Kanał 2: {self.channel2_id}, interwał: {self.interval2}s")
        
        while True:
            try:
                current_time = datetime.now().strftime('%H:%M:%S')
                
                # Serwer 1
                if self.channel1_id:
                    await self.send_message(
                        self.channel1_id, 
                        f"Auto wiadomość #{self.counter1} | Serwer 1 | {current_time}"
                    )
                    self.counter1 += 1
                    await asyncio.sleep(self.interval1)
                
                # Serwer 2
                if self.channel2_id:
                    await self.send_message(
                        self.channel2_id,
                        f"Auto wiadomość #{self.counter2} | Serwer 2 | {current_time}"
                    )
                    self.counter2 += 1
                    await asyncio.sleep(self.interval2)
                    
            except Exception as e:
                print(f"❌ Główny błąd: {e}")
                await asyncio.sleep(60)

async def start_background_tasks(app):
    bot = SimpleSelfBot()
    app['bot_task'] = asyncio.create_task(bot.run_bot())

async def cleanup_background_tasks(app):
    app['bot_task'].cancel()
    await app['bot_task']

if __name__ == "__main__":
    # Uruchom serwer HTTP na porcie 10000
    port = int(os.environ.get('PORT', 10000))
    
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    
    print(f"🚀 Uruchamianie serwera na porcie {port}")
    web.run_app(app, port=port, host='0.0.0.0')
