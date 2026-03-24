import asyncio
import logging
import os
from datetime import datetime, timedelta, timezone

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ChatPermissions

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable not set")

bot = Bot(token=TOKEN)
dp = Dispatcher()


def contains_link(text: str) -> bool:
    if not text:
        return False

    link_keywords = [
        "http://",
        "https://",
        "www.",
        "t.me",
        ".com",
        ".uz",
        ".org",
        ".net",
    ]

    text = text.lower()
    return any(word in text for word in link_keywords)


async def is_admin(chat_id: int, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status in ("administrator", "creator")
    except Exception as e:
        logging.warning(f"Could not check admin status: {e}")
        return False


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


@dp.message(F.text)
async def block_links(message: Message):
    if not message.from_user:
        return

    if not contains_link(message.text):
        return

    if await is_admin(message.chat.id, message.from_user.id):
        return

    try:
        await message.delete()

        until_time = datetime.now(timezone.utc) + timedelta(hours=1)

        permissions = ChatPermissions(
            can_send_messages=False
        )

        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=message.from_user.id,
            permissions=permissions,
            until_date=until_time
        )

    except Exception as e:
        logging.warning(f"Could not restrict user: {e}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())