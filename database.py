from beanie import init_beanie
import motor.motor_asyncio
import os
from models import Team
from dotenv import load_dotenv

load_dotenv()

DB_CONN = os.environ.get("DB_CONN")


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(DB_CONN)
    await init_beanie(database=client.rankings, document_models=[Team])
