from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from dotenv import load_dotenv
import os
load_dotenv()
class DatabaseConnection:
    client: AsyncIOMotorClient
    db: AsyncIOMotorDatabase
      
    @classmethod
    async def connect_and_init(cls):
        cls.client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
        cls.db = cls.client[os.getenv("MONGO_DB")]
        
    @classmethod
    async def close(cls):
        if cls.client:
            cls.client.close()