from typing import List
from beanie import Document
from datetime import datetime
from pydantic import BaseModel, EmailStr


# Users Models
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
    email: EmailStr
    # friends: List[Friend]

    class Settings:
        projection = {"_id": False}


# Message Models
class Message(Document):
    # id: str = Field(hidden_from_schema=True)
    text: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    username: str

    class Settings:
        name = "Messages"


# Requests Models
class FriendsRequests(Document):
    request_sender: str
    request_getter: str

    class Settings:
        name = "FriendsRequests"
