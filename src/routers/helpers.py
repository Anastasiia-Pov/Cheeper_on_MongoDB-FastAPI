from datetime import datetime
import logging
from operator import attrgetter
from models.user_models import User, ReadUser, FriendsRequests, Friend
from fastapi import APIRouter, HTTPException, status, Response, Depends
from beanie.odm.operators.find.logical import Or


# Function to check user's existence in DB
async def check_user_existence(username):
    user = await User.find_one(User.username == username)
    return user if user else None


# Function to check whether two users are already friends
async def check_friendship(request_sender: str,
                           request_getter: str):
    # Find the request_getter in DB
    user_getter = await check_user_existence(request_getter)

    # Check if request_sender is already in request_getter's friends list
    sender_is_friend = any(friend.friend == request_sender for friend in user_getter.friends)

    return sender_is_friend if sender_is_friend else None


# Function to check whether friends request already exists
async def check_friendsrequest(request: FriendsRequests):
    # check if request already exists for both users
    check_requests = await FriendsRequests.find_one(Or(
        {"request_sender": request.request_sender,
         "request_getter": request.request_getter},
        {"request_sender": request.request_getter,
         "request_getter": request.request_sender}))

    return check_requests if check_requests else None
