from fastapi import HTTPException
from fastapi import APIRouter
from mongo_db import Message
import beanie
from datetime import datetime, date


message_router = APIRouter(tags=['Messages'])


# post new message
@message_router.post("/message", summary='Add new message')
async def add_new_message(message: Message):
    """
    message is a class of model Message has the following fields:
    - **id**: exclude id from swagger to avoid double key error
    - **text**: text of a message, type str
    - **created_at**: date and time of posting, type datetime.now()
    - **updated_at**: date and time of updating, type datetime.now()
    - **username**: username, type str
    """
    try:
        result = await Message.insert(message)
        # print(result)
        return {
            "message": "New message created successfully."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# get all messages by username
@message_router.get("/message/{username}", summary='Get all messages')
async def get_messages(username: str):
    """
    - **username**: username, type str
    """
    try:
        result = await Message.find({"username": username}).to_list()
        if result:
            # print(result)
            return result
        else:
            return {"message": "Error 404: No messages found."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# get all messages by username in a given range
@message_router.get("/message_in_range/{username}", summary='Get all messages in a given range')
async def get_messages_in_range(username: str,
                                from_date: datetime,
                                to_date: datetime):
    """
    - **username**: username, type str
    - **from_date**: start of range, type datetime (written in format like YYYY-MM-DD)
    - **to_date**: end of range, type datetime (written in format like YYYY-MM-DD)
    """
    try:
        result = await Message.find(Message.username == username,
                                    from_date <= Message.updated_at <= to_date).to_list()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# get message by id
@message_router.get("/message/{id}", summary='Get message by id')
async def get_messageid(id: str):
    """
    - **id**: id of a message, type str
    """
    try:
        result = await Message.get(id)
        # print(result)
        if result:
            # print(result)
            return result
        else:
            return {"message": "Error 404: No message found."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# edit message by id
@message_router.patch("/message/{id}", summary='Edit message text')
async def edit_message(id: str,
                       upd_text: str,):
    """
    - **id**: id of a message to update, type str
    - **upd_text**: text of an updated message, type str
    """
    try:
        result = await Message.get(id)
        # print(result)
        if result:
            await result.set({Message.text: upd_text,
                              Message.updated_at: datetime.now()})
            return {"message": "Message updated successfully."}
        else:
            return {"message": "Error 404: No message found."}
    except (ValueError, beanie.exceptions.DocumentNotFound):
        return {"message": "Can't replace a non existing document"}


# delete message by id
@message_router.delete("/message/{id}", summary='Delete message by id')
async def delete_message(id: str):
    """
    - **id**: id of a message, type str
    """
    try:
        result = await Message.get(id)
        await result.delete()
        return {"message": "Message deleted successfully."}
    except (ValueError, beanie.exceptions.DocumentNotFound):
        return {"message": "Can't delete a non existing document"}
