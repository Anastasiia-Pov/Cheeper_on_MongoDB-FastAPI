import motor.motor_asyncio
from beanie import init_beanie
from fastapi_users.db import BeanieBaseUser

from models import (User, ReadUser, FriendsRequests,
                    Message, )
from config import MONGO_HOST, MONGO_PORT, MONGO_DB



DATABASE_URL = f"mongodb://{MONGO_HOST}:{MONGO_PORT}"


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
