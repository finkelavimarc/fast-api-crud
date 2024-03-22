import logging
from decouple import config
from fastapi import HTTPException
from auth.crypto_context import CryptoContext
from models.mongo_model import UserRegister
from mongo.db_interface import CrudOperations
import motor.motor_asyncio

class Mongo(CrudOperations):
    """
    MongoDB client for performing CRUD operations.
    """

    def __init__(self, db_url):
        """
        Initialize the MongoDB client and crypto context.

        Args:
            db_url (str): Database connection URL.
        """
        self.db_url = db_url
        self.crypto_context = CryptoContext()

    async def connect(self):
        """
        Connect to the MongoDB database.
        """
        try:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(self.db_url)
            logging.info("Connected to MongoDB")
        except Exception as e:
            logging.error(f"Error connecting to MongoDB: {e}")
            raise HTTPException(status_code=500, detail="HTTP error")

    async def close(self):
        """
        Close the MongoDB client connection.
        """
        try:
            self.client.close()
            logging.info("MongoDB connection closed")
        except Exception as e:
            logging.error(f"Error closing MongoDB connection: {e}")
            raise HTTPException(status_code=500, detail="HTTP error")

    async def find_one(self, collection, filter: dict):
        """
        Find a single document in the specified collection matching the filter.

        Args:
            collection (str): Name of the collection to search.
            filter (dict): Filter criteria.

        Returns:
            dict: Matching document.
        """
        try:
            return await self.client[self.db_url][collection].find_one(filter)
        except Exception as e:
            logging.error(f"Error when searching in db {e}")
            raise HTTPException(status_code=500, detail="HTTP error")

    async def insert(self, collection, element: dict):
        """
        Insert a new document into the specified collection.

        Args:
            collection (str): Name of the collection to insert into.
            element (dict): Document to insert.

        Returns:
            dict: Result of the insertion operation.
        """
        try:
            res = await self.client[self.db_url][collection].insert_one(element)
            logging.info(f"New document inserted into {collection} collection")
            return res
        except Exception as e:
            logging.error(f"Error when inserting data {e}")
            raise HTTPException(status_code=500, detail="HTTP error")


