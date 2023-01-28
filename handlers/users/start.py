from asyncpg.exceptions import UniqueViolationError
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from data.config import ADMINS
from loader import dp, db, bot


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        user = await db.addUser(telegramId=message.from_user.id,
                                fullName=message.from_user.full_name,
                                userName=message.from_user.username)
    except UniqueViolationError:
        user = await db.selectUser(telegramId=message.from_user.id)

    await message.answer(f"Salom, {message.from_user.full_name}!")

    count = await db.countUsers()
    msg = f"@{user[1]} bazaga qo'shildi. \n Bazada {count} ta foydalanuvchi bor."
    await bot.send_message(chat_id=ADMINS[0], text=msg)
