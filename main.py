import discord
import asyncio
import os
import time
from datetime import datetime

class SelfBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(intents=intents, self_bot=True)
        
        # Pobierz ID kanałów z zmiennych środowiskowych
        self.server1_channel_id = int(os.getenv('SERVER1_CHANNEL_ID', 0))
        self.server2_channel_id = int(os.getenv('SERVER2_CHANNEL_ID', 0))
        self.interval = int(os.getenv('INTERVAL_SECONDS', 300))
        
    async def on_ready(self):
        print(f'✅ Zalogowano jako {self.user}')
        print(f'📝 Kanał 1: {self.server1_channel_id}')
        print(f'📝 Kanał 2: {self.server2_channel_id}')
        print(f'⏰ Interwał: {self.interval} sekund')
        self.loop.create_task(self.auto_message_loop())
    
    async def auto_message_loop(self):
        await self.wait_until_ready()
        
        counter = 1
        while not self.is_closed():
            try:
                # Wiadomość dla pierwszego serwera
                if self.server1_channel_id:
                    channel1 = self.get_channel(self.server1_channel_id)
                    if channel1:
                        await channel1.send(f"Test 1 #{counter} | Serwer 1 | {datetime.now().strftime('%H:%M:%S')}")
                        print(f"📤 Wysłano wiadomość #{counter} na kanał 1")
                
                # Wiadomość dla drugiego serwera
                if self.server2_channel_id:
                    channel2 = self.get_channel(self.server2_channel_id)
                    if channel2:
                        await channel2.send(f"Test 2 #{counter} | Serwer 2 | {datetime.now().strftime('%H:%M:%S')}")
                        print(f"📤 Wysłano wiadomość #{counter} na kanał 2")
                
                counter += 1
                print(f"⏳ Oczekiwanie {self.interval} sekund...")
                    
            except Exception as e:
                print(f"❌ Błąd: {e}")
            
            await asyncio.sleep(self.interval)

if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("❌ BRAK TOKENU! Ustaw zmienną DISCORD_TOKEN na Render.com")
    else:
        bot = SelfBot()
        try:
            bot.run(token, bot=False)
        except Exception as e:
            print(f"❌ Błąd uruchomienia: {e}")
