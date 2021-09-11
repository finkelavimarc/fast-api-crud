import motor.motor_asyncio
import logging
from decouple import config
from fastapi import HTTPException
from auth.crypto_context import CryptoContext
from models.mongo_model import UserRegister
from mongo.db_interface import CrudOperations


class Mongo(CrudOperations):
    def __init__(self):
        logging.basicConfig(filename="db_crud.log", level=logging.INFO)
        self.mongo_url = config("mongo_url")
        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.mongo_url).users
        self.crypto_context = CryptoContext()

    async def find_one(self, filter: dict):
        try:
            return await self.client.users.find_one(filter)
        except Exception as e:
            logging.error(f"Error when searching in db {e}")
            raise HTTPException(status_code=500, detail="Http error")

    async def insert(self, element: dict):
        try:
            res = await self.client.users.insert_one(element)
            logging.info("New user in db")
            return res
        except Exception as e:
            logging.error(f"Error when inserting data {e}")
            raise HTTPException(status_code=500, detail="Http error")

    async def _user_exists(self, username: str):
        try:
            return await self.get_user(username)
        except Exception as e:
            logging.error(f"Error when checking users {e}")
            raise HTTPException(status_code=500, detail="Http error")

    async def add_user(self, user: UserRegister) -> dict:
        user_exists = await self._user_exists(user.username)
        if user_exists:
            raise HTTPException(status_code=500, detail="User Already exists")
        if hasattr(user, "id"):
            delattr(user, "id")
        user.password = self.crypto_context.get_password_hash(user.password)
        await self.insert(user.dict(by_alias=True))
        return {"message": f"User {user.username} was inserted"}

    async def get_user(self, username: str):
        return await self.find_one({"username": username})
