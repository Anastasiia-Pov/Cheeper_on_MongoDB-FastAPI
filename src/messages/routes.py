from fastapi import HTTPException
from fastapi import APIRouter
from mongo_db import Message
import beanie
from datetime import datetime


message_router = APIRouter(
    tags=['Messages']
)


# post new message
@message_router.post("/message", summary='Add new message')
async def add_new_message(message: Message):
    try:
        result = await Message.insert(message)
        # print(result)
        return {
            "message": "New message created successfully."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# get all messages by username
@message_router.get("/message", summary='Get all messages')
async def get_messages(username: str):
    try:
        result = await Message.find({"username": username}).to_list()
        if result:
            # print(result)
            return result
        else:
            return {"message": "Error 404: No tasks found."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# get all messages by username


# get message by id
@message_router.get("/message/{id}", summary='Get message by id')
async def get_messageid(id: str):
    try:
        result = await Message.get(id)
        # print(result)
        if result:
            # print(result)
            return result
        else:
            return {"message": "Error 404: No task found."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# edit message by id
@message_router.patch("/message/{id}", summary='Edit message text')
async def edit_message(id: str,
                       upd_text: str,):
    try:
        result = await Message.get(id)
        # print(result)
        if result:
            await result.set({Message.text: upd_text,
                              Message.updated_at: datetime.now()})
            return {"message": "Message updated successfully."}
        else:
            return {"message": "Error 404: No task found."}
    except (ValueError, beanie.exceptions.DocumentNotFound):
        return {"message": "Can't replace a non existing document"}


# delete message by id
@message_router.delete("/message/{id}", summary='Delete message by id')
async def delete_message(id: str):
    try:
        result = await Message.get(id)
        await result.delete()
        return {"message": "Message deleted successfully."}
    except (ValueError, beanie.exceptions.DocumentNotFound):
        return {"message": "Can't delete a non existing document"}
