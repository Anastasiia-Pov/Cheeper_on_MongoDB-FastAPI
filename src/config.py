from pydantic_settings import BaseSettings
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()
BASE_DIR = Path(__file__).parent.parent

MONGO_HOST = os.environ.get("MONGO_HOST")
MONGO_PORT = os.environ.get("MONGO_PORT")
MONGO_DB = os.environ.get("MONGO_DB")

MONGO_HOST_TEST = os.environ.get("MONGO_HOST_TEST")
MONGO_PORT_TEST = os.environ.get("MONGO_PORT_TEST")
MONGO_DB_TEST = os.environ.get("MONGO_DB_TEST")


# Settings for authentification JWT
class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 20
    # access_token_expire_minutes: int = 3


class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
