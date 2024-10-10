from dotenv import load_dotenv
import os

load_dotenv()

MONGO_HOST = os.environ.get("MONGO_HOST")
MONGO_PORT = os.environ.get("MONGO_PORT")
MONGO_DB = os.environ.get("MONGO_DB")
