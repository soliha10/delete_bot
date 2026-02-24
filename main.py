import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()


# Kimdir guruhga qo'shilganda chiqadigan service message'ni o'chirish
@dp.message(F.new_chat_members)
async def delete_join_message(message: Message):
    try:
        await message.delete()
    except Exception as e:
        logging.warning(f"Could not delete join message: {e}")


# Kimdir guruhdan chiqib ketsa chiqadigan service message'ni o'chirish
@dp.message(F.left_chat_member)
async def delete_left_message(message: Message):
    try:
        await message.delete()
    except Exception as e:
        logging.warning(f"Could not delete left message: {e}")


async def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable not set")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())