from dotenv import load_dotenv
import os

load_dotenv()

MONGO_HOST = os.environ.get("MONGO_HOST")
MONGO_PORT = os.environ.get("MONGO_PORT")
MONGO_DB = os.environ.get("MONGO_DB")

MONGO_HOST_TEST = os.environ.get("MONGO_HOST_TEST")
MONGO_PORT_TEST = os.environ.get("MONGO_PORT_TEST")
MONGO_DB_TEST = os.environ.get("MONGO_DB_TEST")
