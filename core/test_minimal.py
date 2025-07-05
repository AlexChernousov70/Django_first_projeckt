from telegram import Bot
import asyncio

async def test():
    bot = Bot("7954492239:AAE9GyKenZ0b6ANX7KwyA-rRVXRpm8AAyws")
    await bot.send_message(chat_id="6050649399", text="Минимальный тест")

asyncio.run(test())