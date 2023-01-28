import asyncio

from utils.db_api.postgresql import Database


async def test():
    db = Database()
    await db.create()

    print("Users jadvalini yaratamiz...")
    await db.dropUsers()
    await db.createTableUsers()
    print("Yaratildi")

    print("Foydalanuvchilarni qo'shamiz")

    await db.addUser("anvar", "sariqdev", 123456789)
    await db.addUser("olim", "olim223", 12341123)
    await db.addUser("1", "1", 131231)
    await db.addUser("1", "1", 23324234)
    await db.addUser("John", "JohnDoe", 4388229)
    print("Qo'shildi")

    users = await db.selectAllUsers()
    print(f"Barcha foydalanuvchilar: {users}")

    user = await db.selectUser(telegramId=123456789)
    print(f"Foydalanuvchi: {user}")


asyncio.run(test())
