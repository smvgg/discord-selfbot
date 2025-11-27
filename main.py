import discord
import asyncio
import os
import time
from datetime import datetime

class SelfBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(intents=intents, self_bot=True)
        
        # Pobierz ID kanałów i interwały z zmiennych środowiskowych
        self.server1_channel_id = int(os.getenv('SERVER1_CHANNEL_ID', 0))
        self.server2_channel_id = int(os.getenv('SERVER2_CHANNEL_ID', 0))
        self.interval1 = int(os.getenv('INTERVAL_SECONDS_1', 300))  # Dla serwera 1
        self.interval2 = int(os.getenv('INTERVAL_SECONDS_2', 300))  # Dla serwera 2
        
        self.counter1 = 1
        self.counter2 = 1
        self.last_message1 = 0
        self.last_message2 = 0
        
    async def on_ready(self):
        print(f'✅ Zalogowano jako {self.user}')
        print(f'📝 Kanał 1: {self.server1_channel_id} | Interwał: {self.interval1}s')
        print(f'📝 Kanał 2: {self.server2_channel_id} | Interwał: {self.interval2}s')
        self.loop.create_task(self.auto_message_loop())
    
    async def auto_message_loop(self):
        await self.wait_until_ready()
        
        while not self.is_closed():
            current_time = time.time()
            
            try:
                # Serwer 1 - sprawdź czy czas na wiadomość
                if self.server1_channel_id and (current_time - self.last_message1) >= self.interval1:
                    channel1 = self.get_channel(self.server1_channel_id)
                    if channel1:
                        await channel1.send(f"Auto wiadomość #{self.counter1} | Serwer 1 | {datetime.now().strftime('%H:%M:%S')}")
                        print(f"📤 Wysłano wiadomość #{self.counter1} na kanał 1 (co {self.interval1}s)")
                        self.counter1 += 1
                        self.last_message1 = current_time
                
                # Serwer 2 - sprawdź czy czas na wiadomość
                if self.server2_channel_id and (current_time - self.last_message2) >= self.interval2:
                    channel2 = self.get_channel(self.server2_channel_id)
                    if channel2:
                        await channel2.send(f"Auto wiadomość #{self.counter2} | Serwer 2 | {datetime.now().strftime('%H:%M:%S')}")
                        print(f"📤 Wysłano wiadomość #{self.counter2} na kanał 2 (co {self.interval2}s)")
                        self.counter2 += 1
                        self.last_message2 = current_time
                    
            except Exception as e:
                print(f"❌ Błąd: {e}")
            
            await asyncio.sleep(10)  # Sprawdzaj co 10 sekund

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
