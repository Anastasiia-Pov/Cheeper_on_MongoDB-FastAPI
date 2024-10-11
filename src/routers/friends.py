from datetime import datetime
import logging
from operator import attrgetter
from models import User, ReadUser, FriendsRequests, Friend
from fastapi import APIRouter, HTTPException
from beanie.odm.operators.find.logical import Or


friends_router = APIRouter(prefix="/friends", tags=["Friends"])
log = logging.getLogger(__name__)


# Function to check whether two users are already friends
async def are_users_friends(request: FriendsRequests):
    # Find both users: the one sending the request and the one accepting it
    user_sender = await User.find_one(User.username == request.request_sender)
    user_getter = await User.find_one(User.username == request.request_getter)
    if not user_sender or not user_getter:
        raise HTTPException(status_code=400, detail="Bad request: user not found")

    # Check if request_sender is already in request_getter's friends list
    sender_is_friend = any(friend.friend == request.request_sender for friend in user_getter.friends)

    if sender_is_friend:
        return True  # Users are already friends
    return False  # Users are not friends


# Function to check whether friends request already exists
async def are_friendsrequest(request: FriendsRequests):
    # check if request already exists for both users
    check_requests = await FriendsRequests.find_one(Or({"request_sender": request.request_sender,
                                                        "request_getter": request.request_getter},
                                                       {"request_sender": request.request_getter,
                                                        "request_getter": request.request_sender}))
    if check_requests:  # request already exists
        return True  # Error 409 Conflict: Request already exists
    return False  # Request was not found


# post friend's requests
@friends_router.post("/requests/{username}", summary="Send friends request")
async def send_request(request: FriendsRequests):
    """
    request is a class of model FriendsRequests has the following fields:
    - **id**: exclude id from swagger to avoid double key error
    - **request_sender**: username of a user who sends request, type str
    - **request_getter**: username of a user who gets request, type str
    """
    try:
        # check if users are already friends
        friendship_check = await are_users_friends(request)
        if friendship_check:
            return {"message": "Users are already friends"}

        # check if there is no friends requests between users
        request_check = await are_friendsrequest(request)
        if request_check:
            return {"message": "Error 409 Conflict: Request already exists."}

        # if above conditions are verified send query to create friendsrequest
        result = await User.find_one({"username": request.request_getter})
        if result:
            await FriendsRequests.insert(request)
            return {"message": "Friend request was sent successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# get all friends requests by username
@friends_router.get("/requests/{username}", summary="Get friend requests")
async def get_request(username: str):
    """
    - **username**: username of a user
    """
    try:
        # get all request for username as a sender and as a getter
        result = await FriendsRequests.find_many(Or(FriendsRequests.request_getter==username,
                                                    FriendsRequests.request_sender==username)).to_list()
        if result:
            return result
        else:
            return {"message": "Error 404: No friends requests were found."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# accept friends request
@friends_router.patch("/requests", summary="Accept friends request")
async def accept_request(request: FriendsRequests):
    """
    request is a class of model FriendsRequests has the following fields:
    - **id**: exclude id from swagger to avoid double key error
    - **request_sender**: username of a user who sends request, type str
    - **request_getter**: username of a user who gets request, type str
    """
    try:
        # check if users are already friends
        friendship_check = await are_users_friends(request)
        if friendship_check:
            return {"message": "Users are already friends"}

        # check if there is no friends requests between users
        request_check = await are_friendsrequest(request)
        if not request_check:
            return {"message": "Request was not found"}

        # Create new Friend objects for both users
        sender_friend = Friend(friend=request.request_getter,
                               friendship_date=datetime.now())
        getter_friend = Friend(friend=request.request_sender,
                               friendship_date=datetime.now())

        # Add the request_getter to the request_sender's friends list
        await User.find_one(User.username == request.request_sender).update({
            "$push": {"friends": sender_friend.dict()}})
        # Add the request_sender to the request_getter's friends list
        await User.find_one(User.username == request.request_getter).update({
            "$push": {"friends": getter_friend.dict()}})
        # Delete for FriendsRequests Collection
        check_request1 = await FriendsRequests.find_one(Or(
            {"request_sender": request.request_sender,
             "request_getter": request.request_getter},
            {"request_sender": request.request_getter,
             "request_getter": request.request_sender})
            )
        await check_request1.delete()
        log.warning({"message": f"Request for {request.request_sender} and {request.request_getter} is deleted from FriendsRequests collection."})
        return {"message": f"{request.request_sender} and {request.request_getter} are now friends!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# get user's friends
@friends_router.get("/{username}", summary="Get user's friends")
async def get_friends(username):
    """
    - **username**: username of a user
    """
    try:
        result = await User.find_one(User.username == username)
        if result:
            friends_list = result.friends
            return sorted(friends_list, key=attrgetter('friendship_date'))
        else:
            return {"message": "Error 404: No user found."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# get number of user's friends
@friends_router.get("/numfriends/{username}", summary="Get number of user's friends")
async def get_numfriends(username):
    """
    - **username**: username of a user
    """
    try:
        result = await User.find_one(User.username == username)
        if result:
            friends_list = result.friends
            return f"User {username} has {len(friends_list)} friends"
        else:
            return {"message": "Error 404: No user found."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
