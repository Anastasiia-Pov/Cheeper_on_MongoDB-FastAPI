import beanie
from fastapi import Depends, Request
from typing import Annotated
from mongo_db import Message
from datetime import datetime
from models.user_models import User
from routers.helpers import check_user_existence
from auth.validation import get_current_token_payload, oauth2_scheme
from fastapi import APIRouter, HTTPException, status, Response


message_router = APIRouter(prefix="/messages",
                           tags=['Messages'],
                           dependencies=[Depends(oauth2_scheme)])


# post new message
@message_router.post("/new",
                     status_code=status.HTTP_201_CREATED,
                     summary='Add new message')
async def add_new_message(message: Message,
                          payload: dict = Depends(get_current_token_payload)) -> dict:
    try:
        await Message.insert(message)
        return {"message": "New message created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# get all messages by username
@message_router.get("/by_username/{username}",
                    status_code=status.HTTP_200_OK,
                    summary='Get all messages')
async def get_messages(username: str,
                       response: Response,
                       payload: dict = Depends(get_current_token_payload)):
    try:
        result = await Message.find({"username": username}).to_list()
        if result and await check_user_existence(username):
            return result
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Messages not found or user does not exists."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# get all messages by username in a given range
@message_router.get("/in_range/{username}",
                    status_code=status.HTTP_200_OK,
                    summary='Get all messages in a given range')
async def get_messages_in_range(username: str,
                                from_date: datetime,
                                to_date: datetime,
                                response: Response,
                                payload: dict = Depends(get_current_token_payload)):
    try:
        result = await Message.find({"username": username,
                                     "updated_at": {"$gte": from_date,
                                                    "$lte": to_date}}).to_list()
        if len(result) == 0:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "User has no messages in a given range."}
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# get message by id
@message_router.get("/by_id/{id}",
                    status_code=status.HTTP_200_OK,
                    summary='Get message by id')
async def get_message_by_id(id: str,
                            response: Response,
                            payload: dict = Depends(get_current_token_payload)):
    try:
        result = await Message.get(id)
        if result:
            return result
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "No message found."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# edit message by id
@message_router.patch("/update/{id}",
                      status_code=status.HTTP_201_CREATED,
                      summary='Edit message text')
async def edit_message(id: str,
                       upd_text: str,
                       response: Response,
                       payload: dict = Depends(get_current_token_payload)):
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


# like a message
@message_router.patch("/like/{message_id}",
                      status_code=status.HTTP_200_OK,
                      summary='Like a message')
async def like_message(message_id: str,
                       username: str,
                       response: Response,
                       payload: dict = Depends(get_current_token_payload)):
    try:
        # Check if the message and user exist
        check_message_exists = await Message.get(message_id)
        get_user = await check_user_existence(username)

        if check_message_exists and get_user:
            # Check if the user has already liked the message
            if (username not in check_message_exists.likes) and (message_id not in get_user.liked_posts):
                # Add username to the list of likes for the message
                check_message_exists.likes.append(username)
                await check_message_exists.save()
                get_user.liked_posts.append(message_id)
                await get_user.save()
                return {"message": "Liked"}
            response.status_code = status.HTTP_409_CONFLICT
            return {"message": "Message was already liked."}
        # If the message or user is not found
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "No message or user found."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@message_router.get("/liked/{username}",
                    status_code=status.HTTP_200_OK,
                    summary='Liked messages')
async def get_liked_messaged(username: str,
                             response: Response,
                             payload: dict = Depends(get_current_token_payload)):
    try:
        check_user = await check_user_existence(username)
        if check_user:
            if len(check_user.liked_posts) == 0:
                response.status_code = status.HTTP_404_NOT_FOUND
                return {"message": "User has not liked any posts yet."}
            return check_user.liked_posts
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "User is not found."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# delete message by id
@message_router.delete("/delete/{id}",
                       status_code=status.HTTP_200_OK,
                       summary='Delete message by id')
async def delete_message(id: str,
                         response: Response,
                         payload: dict = Depends(get_current_token_payload)):
    try:
        result = await Message.get(id)
        if result:
            await result.delete()
            return {"message": "Message deleted successfully."}
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "No message found."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
