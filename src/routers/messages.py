import beanie
from mongo_db import Message
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Response


message_router = APIRouter(tags=['Messages'])


# post new message
@message_router.post("/messages",
                     status_code=status.HTTP_201_CREATED,
                     summary='Add new message')
async def add_new_message(message: Message):
    try:
        await Message.insert(message)
        return {"message": "New message created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# get all messages by username
@message_router.get("/messages/{username}",
                    status_code=status.HTTP_200_OK,
                    summary='Get all messages')
async def get_messages(username: str,
                       response: Response):
    try:
        result = await Message.find({"username": username}).to_list()
        if result:
            return result
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "No messages found."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# get all messages by username in a given range
@message_router.get("/messages_in_range/{username}",
                    status_code=status.HTTP_200_OK,
                    summary='Get all messages in a given range')
async def get_messages_in_range(username: str,
                                from_date: datetime,
                                to_date: datetime,
                                response: Response):
    try:
        result = await Message.find({"username": username,
                                     "updated_at": {"$gte": from_date,
                                                    "$lte": to_date}}).to_list()
        if len(result) == 0:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "User has not written any messages yet."}
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# get message by id
@message_router.get("/message/{id}",
                    status_code=status.HTTP_200_OK,
                    summary='Get message by id')
async def get_message_by_id(id: str,
                            response: Response):
    try:
        result = await Message.get(id)
        if result:
            return result
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "No message found."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# edit message by id
@message_router.patch("/message/{id}",
                      status_code=status.HTTP_201_CREATED,
                      summary='Edit message text')
async def edit_message(id: str,
                       upd_text: str,
                       response: Response):
    try:
        result = await Message.get(id)
        if result:
            await result.set({Message.text: upd_text,
                              Message.updated_at: datetime.now()})
            return {"message": "Message updated successfully."}
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "No message found."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# delete message by id
@message_router.delete("/message/{id}",
                       status_code=status.HTTP_200_OK,
                       summary='Delete message by id')
async def delete_message(id: str,
                         response: Response):
    try:
        result = await Message.get(id)
        if result:
            await result.delete()
            return {"message": "Message deleted successfully."}
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "No message found."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
