import logging
from datetime import datetime
from operator import attrgetter
from beanie.odm.operators.find.logical import Or
from fastapi import APIRouter, HTTPException, status, Response, Depends

from auth.validation import get_current_token_payload, oauth2_scheme
from models.user_models import User, ReadUser, FriendsRequests, Friend
from routers.helpers import check_friendship, check_user_existence, check_friendsrequest


friends_router = APIRouter(prefix="/friends",
                           tags=["Friends"],
                           dependencies=[Depends(oauth2_scheme)])
log = logging.getLogger(__name__)


# post friend's requests
@friends_router.post("/requests/{username}",
                     status_code=status.HTTP_201_CREATED,
                     summary="Send friends request")
async def send_request(request: FriendsRequests,
                       response: Response,
                       payload: dict = Depends(get_current_token_payload)):
    try:
        # check if users exists
        user_sender = await check_user_existence(request.request_sender)
        user_getter = await check_user_existence(request.request_getter)
        if not user_sender or not user_getter:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "User not found."}

        # check if users are already friends
        are_users_friends = await check_friendship(request.request_sender,
                                                   request.request_getter)
        if are_users_friends:
            response.status_code = status.HTTP_409_CONFLICT
            return {"message": "Users are already friends"}

        # check if there is no friends requests between users
        is_request = await check_friendsrequest(request)
        if is_request:
            response.status_code = status.HTTP_409_CONFLICT
            return {"message": "Request already exists."}

        # if above conditions are verified send query to create friendsrequest
        await FriendsRequests.insert(request)
        return {"message": "Friend request was sent successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# get all friends requests by username
@friends_router.get("/requests/{username}",
                    status_code=status.HTTP_200_OK,
                    summary="Get friend requests")
async def get_request(username: str,
                      response: Response,
                      payload: dict = Depends(get_current_token_payload)):
    try:
        # check if users exists
        user_exists = await check_user_existence(username)
        if not user_exists:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "User not found"}

        # get all request for username as a sender and as a getter
        result = await FriendsRequests.find_many(Or(FriendsRequests.request_getter==username,
                                                    FriendsRequests.request_sender==username)).to_list()
        if result:
            return result
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "No friends requests were found."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# accept friends request
@friends_router.patch("/requests",
                      status_code=status.HTTP_200_OK,
                      summary="Accept friends request")
async def accept_request(request: FriendsRequests,
                         response: Response,
                         payload: dict = Depends(get_current_token_payload)):
    try:
        # check if users exists
        user_sender = await check_user_existence(request.request_sender)
        user_getter = await check_user_existence(request.request_getter)
        if not user_sender or not user_getter:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "User not found"}

        # check if users are already friends
        friendship_check = await check_friendship(request.request_sender,
                                                  request.request_getter)
        if friendship_check:
            response.status_code = status.HTTP_409_CONFLICT
            return {"message": "Users are already friends"}

        # check if there is no friends requests between users
        request_check = await check_friendsrequest(request)
        if not request_check:
            response.status_code = status.HTTP_404_NOT_FOUND
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
@friends_router.get("/{username}",
                    status_code=status.HTTP_200_OK,
                    summary="Get user's friends")
async def get_friends(username: str,
                      response: Response,
                      payload: dict = Depends(get_current_token_payload)):
    try:
        result = await check_user_existence(username)
        if result:
            friends_list = result.friends
            return sorted(friends_list, key=attrgetter('friendship_date'))
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "No user found."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# get number of user's friends
@friends_router.get("/numfriends/{username}",
                    status_code=status.HTTP_200_OK,
                    summary="Get number of user's friends")
async def get_num_of_friends(username,
                             response: Response,
                             payload: dict = Depends(get_current_token_payload)):
    try:
        result = await check_user_existence(username)
        if result:
            friends_list = result.friends
            return f"User {username} has {len(friends_list)} friends"
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "No user found."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
