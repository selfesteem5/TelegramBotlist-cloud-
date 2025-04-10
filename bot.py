from telethon.sync import TelegramClient
from telethon.errors import (
    FloodWaitError, 
    UsernameNotOccupiedError,
    UsernameInvalidError
)
from telethon.tl.functions.contacts import ResolveUsernameRequest
import random
import string
import asyncio

# ========== إعداداتك ========== #
api_id = 23696693
api_hash = '1ed9da3506e9b880ddcc09edf6a3c25e'
bot_token = '7734614727:AAH9ayViSlxwNPBz8bGN66gaaCBXEfpTNP0'
your_id = 5098723231
# ============================== #

client = TelegramClient('session_name', api_id, api_hash)

def generate_smart_username(length):
    """توليد يوزرات مميزة بتكرارات ذكية حسب الطول"""
    patterns = [
        # نمط 1: تكرار أحرف + أرقام (aaaa111)
        lambda l: random.choice(string.ascii_lowercase)*(l-3) + str(random.randint(100,999)),
        
        # نمط 2: كلمات مميزة مقطوعة (drag202)
        lambda l: random.choice(['dragon','phantom','galaxy','titan','nexus'])[:l-3] + str(random.randint(100,999)),
        
        # نمط 3: أرقام في المنتصف (a1a2a3)
        lambda l: ''.join([random.choice(string.ascii_lowercase) if i%2==0 else str(random.randint(0,9)) for i in range(l)]),
        
        # نمط 4: ماركات عالمية (nike5)
        lambda l: random.choice(['nike','adidas','apple','samsung','tesla'])[:l-1] + str(random.randint(1,9))
    ]
    return random.choice(patterns)(length)

async def precise_check(username):
    """فحص دقيق للنوع مع التعرف على المدفوع"""
    try:
        result = await client(ResolveUsernameRequest(username=username))
        if result.users and result.users[0].premium:
            return '💰 مدفوع'
        return '❌ مُستخدم'
    except UsernameNotOccupiedError:
        return '✅ متاح'
    except UsernameInvalidError:
        return '⚠️ غير صالح'
    except Exception:
        return '⚠️ خطأ'

async def smart_generator():
    """مولد ذكي لجميع الأطوال مع إحصاءات"""
    await client.start(bot_token=bot_token)
    await client.send_message(your_id, "🚀 البوت يعمل الآن!")
    
    while True:
        for length in [5, 6, 7, 8]:
            for _ in range(200):  # 200 محاولة لكل طول
                username = generate_smart_username(length)
                status = await precise_check(username)
                
                # إرسال الإشعارات للمستخدم
                if status == '✅ متاح':
                    await client.send_message(
                        your_id, 
                        f"🎉 يوزر {length} أحرف متاح!\n@{username}"
                    )
                
                # عرض النتائج مع التنسيق
                print(f"║ {status} @{username.ljust(15)} (الطول: {length})")
                
                # تأخير ذكي ضد الحظر
                await asyncio.sleep(random.uniform(3, 7))

async def main():
    try:
        await smart_generator()
    except FloodWaitError as e:
        print(f"⏳ تم إيقاف البوت لمدة {e.seconds} ثانية")
        await asyncio.sleep(e.seconds)
        await main()

if __name__ == "__main__":
    asyncio.run(main())