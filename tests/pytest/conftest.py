import pytest
from src.main import app
from beanie import init_beanie
from asgi_lifespan import LifespanManager
from httpx import AsyncClient, ASGITransport
from src.models import Message, User, FriendsRequests
from src.config import MONGO_DB_TEST, MONGO_HOST_TEST, MONGO_PORT_TEST


DATABASE_URL = f"mongodb://{MONGO_HOST_TEST}:{MONGO_PORT_TEST}"


@pytest.fixture
async def client_test():
    # Setup MongoDB connection for the test
    # client = AsyncIOMotorClient(DATABASE_URL)
    # test_db = client[MONGO_DB_TEST]

    # # Initialize Beanie with the test database
    # await init_beanie(database=test_db, document_models=[Message,
    #                                                      User,
    #                                                      FriendsRequests])

    async with LifespanManager(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test", follow_redirects=True) as ac:
            yield ac
