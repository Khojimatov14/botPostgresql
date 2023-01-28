from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config

class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def createTableUsers(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        fullName VARCHAR(255) NOT NULL,
        userName varchar(255) NULL,
        telegramId BIGINT NOT NULL UNIQUE 
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def formatArgs(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def addUser(self, fullName, userName, telegramId):
        sql = "INSERT INTO users (fullName, userName, telegramId) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, fullName, userName, telegramId, fetchrow=True)

    async def selectAllUsers(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def selectUser(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.formatArgs(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def countUsers(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def updateUserUsername(self, userName, telegramId):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, userName, telegramId, execute=True)

    async def deleteUsers(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def dropUsers(self):
        await self.execute("DROP TABLE Users", execute=True)





