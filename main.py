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
        
        # Konfiguracja kanałów z indywidualnymi interwałami
        self.channels_config = {
            # AD ZONE
            os.getenv('AD_ZONE_CHANNEL_1'): {
                "name": "AD ZONE Partnerstwo",
                "interval": int(os.getenv('AD_ZONE_CHANNEL_1_INTERVAL', 300))
            },
            os.getenv('AD_ZONE_CHANNEL_2'): {
                "name": "AD ZONE J4J", 
                "interval": int(os.getenv('AD_ZONE_CHANNEL_2_INTERVAL', 300))
            },
            os.getenv('AD_ZONE_CHANNEL_3'): {
                "name": "AD ZONE Kanał 3",
                "interval": int(os.getenv('AD_ZONE_CHANNEL_3_INTERVAL', 300))
            },
            os.getenv('AD_ZONE_CHANNEL_4'): {
                "name": "AD ZONE Kanał 4",
                "interval": int(os.getenv('AD_ZONE_CHANNEL_4_INTERVAL', 300))
            },
            os.getenv('AD_ZONE_CHANNEL_5'): {
                "name": "AD ZONE Kanał 5",
                "interval": int(os.getenv('AD_ZONE_CHANNEL_5_INTERVAL', 300))
            },
            os.getenv('AD_ZONE_CHANNEL_6'): {
                "name": "AD ZONE Kanał 6",
                "interval": int(os.getenv('AD_ZONE_CHANNEL_6_INTERVAL', 300))
            },
            os.getenv('AD_ZONE_CHANNEL_7'): {
                "name": "AD ZONE Kanał 7",
                "interval": int(os.getenv('AD_ZONE_CHANNEL_7_INTERVAL', 300))
            },
            os.getenv('AD_ZONE_CHANNEL_8'): {
                "name": "AD ZONE Kanał 8",
                "interval": int(os.getenv('AD_ZONE_CHANNEL_8_INTERVAL', 300))
            },
            
            # ZIMOWE REKLAMY
            os.getenv('ZIMOWE_CHANNEL_1'): {
                "name": "Zimowe Reklamy Kanał 1",
                "interval": int(os.getenv('ZIMOWE_CHANNEL_1_INTERVAL', 300))
            },
            os.getenv('ZIMOWE_CHANNEL_2'): {
                "name": "Zimowe Reklamy Kanał 2",
                "interval": int(os.getenv('ZIMOWE_CHANNEL_2_INTERVAL', 300))
            },
            os.getenv('ZIMOWE_CHANNEL_3'): {
                "name": "Zimowe Reklamy Kanał 3",
                "interval": int(os.getenv('ZIMOWE_CHANNEL_3_INTERVAL', 300))
            },
            os.getenv('ZIMOWE_CHANNEL_4'): {
                "name": "Zimowe Reklamy Kanał 4",
                "interval": int(os.getenv('ZIMOWE_CHANNEL_4_INTERVAL', 300))
            },
            os.getenv('ZIMOWE_CHANNEL_5'): {
                "name": "Zimowe Reklamy Kanał 5",
                "interval": int(os.getenv('ZIMOWE_CHANNEL_5_INTERVAL', 300))
            },
            os.getenv('ZIMOWE_CHANNEL_6'): {
                "name": "Zimowe Reklamy Kanał 6",
                "interval": int(os.getenv('ZIMOWE_CHANNEL_6_INTERVAL', 300))
            },
            os.getenv('ZIMOWE_CHANNEL_7'): {
                "name": "Zimowe Reklamy Kanał 7",
                "interval": int(os.getenv('ZIMOWE_CHANNEL_7_INTERVAL', 300))
            },
            os.getenv('ZIMOWE_CHANNEL_8'): {
                "name": "Zimowe Reklamy Kanał 8",
                "interval": int(os.getenv('ZIMOWE_CHANNEL_8_INTERVAL', 300))
            },
            
            # MAGICZNE REKLAMY
            os.getenv('MAGICZNE_CHANNEL_1'): {
                "name": "Magiczne Reklamy Kanał 1",
                "interval": int(os.getenv('MAGICZNE_CHANNEL_1_INTERVAL', 300))
            },
            os.getenv('MAGICZNE_CHANNEL_2'): {
                "name": "Magiczne Reklamy Kanał 2",
                "interval": int(os.getenv('MAGICZNE_CHANNEL_2_INTERVAL', 300))
            },
            os.getenv('MAGICZNE_CHANNEL_3'): {
                "name": "Magiczne Reklamy Kanał 3",
                "interval": int(os.getenv('MAGICZNE_CHANNEL_3_INTERVAL', 300))
            },
            os.getenv('MAGICZNE_CHANNEL_4'): {
                "name": "Magiczne Reklamy Kanał 4",
                "interval": int(os.getenv('MAGICZNE_CHANNEL_4_INTERVAL', 300))
            },
            os.getenv('MAGICZNE_CHANNEL_5'): {
                "name": "Magiczne Reklamy Kanał 5",
                "interval": int(os.getenv('MAGICZNE_CHANNEL_5_INTERVAL', 300))
            },
            os.getenv('MAGICZNE_CHANNEL_6'): {
                "name": "Magiczne Reklamy Kanał 6",
                "interval": int(os.getenv('MAGICZNE_CHANNEL_6_INTERVAL', 300))
            },
            os.getenv('MAGICZNE_CHANNEL_7'): {
                "name": "Magiczne Reklamy Kanał 7",
                "interval": int(os.getenv('MAGICZNE_CHANNEL_7_INTERVAL', 300))
            },
            os.getenv('MAGICZNE_CHANNEL_8'): {
                "name": "Magiczne Reklamy Kanał 8",
                "interval": int(os.getenv('MAGICZNE_CHANNEL_8_INTERVAL', 300))
            }
        }
        
        # Usuń puste kanały (te których nie ustawiono)
        self.active_channels = {channel_id: config for channel_id, config in self.channels_config.items() if channel_id}
        
        self.session = None
        self.counters = {channel_id: 1 for channel_id in self.active_channels}
        self.last_message = {channel_id: 0 for channel_id in self.active_channels}
        
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
            print(f"📤 Próba wysłania: {content} na {self.active_channels[channel_id]['name']}")
            async with self.session.post(url, json=data) as response:
                if response.status == 200:
                    print(f"✅ Wiadomość wysłana na {self.active_channels[channel_id]['name']}")
                    return True
                else:
                    text = await response.text()
                    print(f"❌ Błąd {response.status} na {self.active_channels[channel_id]['name']}: {text}")
                    return False
        except Exception as e:
            print(f"❌ Błąd wysyłania na {self.active_channels[channel_id]['name']}: {e}")
            return False
    
    async def run_bot(self):
        print("🟡 Uruchamianie selfbota z indywidualnymi interwałami dla każdego kanału...")
        
        # Logowanie konfiguracji
        for channel_id, config in self.active_channels.items():
            print(f"📝 {config['name']}: co {config['interval']}s")
        
        while True:
            try:
                current_time = time.time()
                
                for channel_id, config in self.active_channels.items():
                    # Sprawdź czy czas na wiadomość dla tego kanału
                    if (current_time - self.last_message[channel_id]) >= config['interval']:
                        
                        success = await self.send_message(
                            channel_id, 
                            f"Magiczne Reklamy Test #{self.counters[channel_id]}"
                        )
                        
                        if success:
                            self.counters[channel_id] += 1
                            self.last_message[channel_id] = current_time
                            print(f"⏳ {config['name']}: Następna wiadomość za {config['interval']}s")
                    
                # Sprawdź co 10 sekund
                await asyncio.sleep(10)
                    
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
