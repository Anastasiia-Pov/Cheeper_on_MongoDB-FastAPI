from typing import List
from beanie import Document
from datetime import datetime
from pydantic import BaseModel
from bson.objectid import ObjectId


class Message(Document):
    # id: str = Field(hidden_from_schema=True)
    text: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    username: str
    likes: List[str] = []

    class Settings:
        name = "Messages"
