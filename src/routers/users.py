import logging
from service import hash_password, pass_validation
from mongo_db import User, ReadUser
from fastapi import APIRouter, HTTPException, status, Response


auth_router = APIRouter(prefix="/regist", tags=["Regist"])
log = logging.getLogger(__name__)


# post new user
@auth_router.post("/user",
                  status_code=status.HTTP_201_CREATED,
                  summary='Add new user')
async def add_new_user(new_user: User,
                       response: Response):
    try:
        result = await User.find_one(User.username == new_user.username)
        if result:
            response.status_code = status.HTTP_409_CONFLICT
            return {"message": "Username already registered. Please, change username."}
        else:
            check_password = await pass_validation(new_user.hashed_password)
            if check_password:
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {"message": check_password}
            new_user.hashed_password = await hash_password(new_user.hashed_password)
            result = await User.insert(new_user)
            return {"message": "New user created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# get user info by username
@auth_router.get("/user/{username}", summary='Get user info')
async def get_user(username: str):
    try:
        result = await User.find_one({"username": username}).project(ReadUser)
        if result:
            return result
        else:
            return {"message": "Error 404: No user found."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
