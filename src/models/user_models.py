from typing import List
from beanie import Document
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


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
    liked_posts: List[str] = []
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Settings:
        name = "Users"


class ReadUser(BaseModel):
    name: str
    username: str
    email: EmailStr
    # friends: List[Friend]

    class Settings:
        projection = {"_id": False}


# Requests Models
class FriendsRequests(Document):
    request_sender: str
    request_getter: str

    class Settings:
        name = "FriendsRequests"


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True
