import asyncio
import logging
import os
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ChatPermissions

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()


# link aniqlash
def contains_link(text: str) -> bool:
    if not text:
        return False

    link_keywords = [
        "http://",
        "https://",
        "t.me",
        ".com",
        ".uz",
        ".org",
        ".net",
    ]

    text = text.lower()

    return any(word in text for word in link_keywords)


@dp.message(F.new_chat_members)
async def delete_join_message(message: Message):
    try:
        await message.delete()
    except Exception as e:
        logging.warning(f"Could not delete join message: {e}")


@dp.message(F.left_chat_member)
async def delete_left_message(message: Message):
    try:
        await message.delete()
    except Exception as e:
        logging.warning(f"Could not delete left message: {e}")


# link yuborilsa o'chirish va mute qilish
@dp.message(F.text)
async def block_links(message: Message):

    if contains_link(message.text):

        try:
            # xabarni o'chirish
            await message.delete()

            # 1 soat mute
            until_time = datetime.now() + timedelta(hours=1)

            permissions = ChatPermissions(
                can_send_messages=False
            )

            await bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=message.from_user.id,
                permissions=permissions,
                until_date=until_time
            )

            await message.answer(
                f"{message.from_user.full_name} link yuborgani uchun 1 soatga mute qilindi."
            )

        except Exception as e:
            logging.warning(f"Could not restrict user: {e}")


async def main():

    if not TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable not set")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())