import asyncio
import os
from datetime import datetime
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from keep_alive import keep_alive

# تحميل المتغيرات من ملف .env
load_dotenv()

# بيانات البوت
BOT_TOKEN = "7675038991:AAHZhCYRCKESH_o7lc9HNndC42cd9Mys2K8"
MONITOR_CHANNEL = "@xqrrp"  # اسم القناة مع @

class AutoSender:
    def __init__(self):
        self.bot = Bot(token=BOT_TOKEN)
        self.dp = Dispatcher()
        self.current_bio_index = 1
        self.current_hisryat_index = 1
        self.current_magtae_index = 1

    async def initialize(self):
        """تهيئة البوت"""
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - تم تشغيل البوت بنجاح!")

    async def send_message(self, text):
        """إرسال رسالة إلى القناة"""
        try:
            await self.bot.send_message(chat_id=MONITOR_CHANNEL, text=text)
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - تم إرسال: {text}")
        except Exception as e:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - فشل في الإرسال: {e}")

    async def send_bio(self):
        """إرسال أمر البايو"""
        text = f"بايو{self.current_bio_index}"
        await self.send_message(text)
        self.current_bio_index = self.current_bio_index + 1 if self.current_bio_index < 20 else 1

    async def send_hisryat(self):
        """إرسال أمر الحصريات"""
        text = f"حصريات{self.current_hisryat_index}"
        await self.send_message(text)
        self.current_hisryat_index = self.current_hisryat_index + 1 if self.current_hisryat_index < 20 else 1

    async def send_magtae(self):
        """إرسال أمر المقاطع"""
        text = f"مقاطع{self.current_magtae_index}"
        await self.send_message(text)
        self.current_magtae_index = self.current_magtae_index + 1 if self.current_magtae_index < 20 else 1

    async def schedule_tasks(self):
        """جدولة المهام"""
        # بدء مهمة البايو فوراً (كل ساعة)
        await asyncio.sleep(1)
        await self.send_bio()
        asyncio.create_task(self.run_every(self.send_bio, 3600))
        
        # بدء مهمة الحصريات بعد 20 دقيقة (كل ساعة)
        await asyncio.sleep(1200)
        await self.send_hisryat()
        asyncio.create_task(self.run_every(self.send_hisryat, 3600))
        
        # بدء مهمة المقاطع بعد 40 دقيقة (كل ساعة)
        await asyncio.sleep(1200)
        await self.send_magtae()
        asyncio.create_task(self.run_every(self.send_magtae, 3600))

    async def run_every(self, func, interval):
        """تشغيل وظيفة كل فترة زمنية محددة"""
        while True:
            await asyncio.sleep(interval)
            await func()

    async def run(self):
        """تشغيل البوت"""
        await self.initialize()
        await self.schedule_tasks()
        
        # إبقاء البوت يعمل
        while True:
            await asyncio.sleep(3600)

async def main():
    # تشغيل خادم keep_alive
    keep_alive()
    
    sender = AutoSender()
    while True:
        try:
            await sender.run()
        except Exception as e:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - حدث خطأ: {e}")
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - إعادة التشغيل بعد 60 ثانية...")
            await asyncio.sleep(60)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - تم إيقاف البرنامج")
