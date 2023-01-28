import asyncio
from aiogram.types import Message
from data.config import ADMINS
from loader import dp, db, bot

@dp.message_handler(commands=("reklama"), user_id= ADMINS)
async def sendAdToAll(message: Message):
    users = await db.selectAllUsers()
    for user in users:
        await bot.send_message(chat_id=user[3], text="Bu yerda reklama bor")
        await asyncio.sleep(0.05)
