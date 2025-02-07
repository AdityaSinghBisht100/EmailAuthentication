from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from dotenv import load_dotenv
import os

load_dotenv()

client: AsyncIOMotorClient = None
db: AsyncIOMotorDatabase = None

async def connect_and_init():
    global client, db
    client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
    db = client[os.getenv("MONGO_DB")]

async def close():
    if client:
        client.close()
