from typing import List, Optional
import motor.motor_asyncio
from beanie import Document
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase
from config import MONGO_HOST, MONGO_PORT, MONGO_DB
from datetime import datetime
from beanie import init_beanie
from pydantic import Field, BaseModel, SecretStr, EmailStr
from pydantic.json_schema import SkipJsonSchema


DATABASE_URL = f"mongodb://{MONGO_HOST}:{MONGO_PORT}"


class Message(Document):
    # id: str = Field(hidden_from_schema=True)
    text: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    username: str

    class Settings:
        name = "Messages"


class Friend(BaseModel):
    friend: str
    friendship_date: datetime = datetime.now()


class User(Document):
    """User database representation"""
    name: str
    username: str
    email: EmailStr
    hashed_password: str
    created_at: datetime = datetime.now()
    friends: List[Friend] = []
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Settings:
        name = "Users"


class ReadUser(BaseModel):
    name: str
    username: str
    created_at: datetime
    email: EmailStr
    friends: List[Friend]

    class Settings:
        projection = {"_id": False}


class FriendsRequests(Document):
    request_sender: str
    request_getter: str

    class Settings:
        name = "FriendsRequests"


async def get_user_db():
    yield BeanieUserDatabase(User)


# method for start the MongoDb Connection
async def startup_db_client(app):
    app.mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
    app.mongodb = app.mongodb_client.get_database(MONGO_DB)
    await init_beanie(database=app.mongodb,
                      document_models=[Message, User, FriendsRequests],)
    print("MongoDB connected.")


# method to close the database connection
# async def shutdown_db_client(app):
#     app.mongodb_client.close()
#     print("Database disconnected.")
