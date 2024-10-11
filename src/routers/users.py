import logging
from service import hash_password, pass_validation
from mongo_db import User, ReadUser
from fastapi import APIRouter, HTTPException


auth_router = APIRouter(prefix="/auth", tags=["Auth"])
log = logging.getLogger(__name__)


# post new user
@auth_router.post("/user", summary='Add new user')
async def add_new_user(new_user: User):
    """
    new_user is a class of model User has the following fields:
    - **id**: exclude id from swagger to avoid double key error
    - **name**: name of a new user, type str
    - **username**: username of a user, type str
    - **email**: email of a user, type EmailStr
    - **hashed_password**: email of a user, type str
    - **created_at**: datetime of creating a user, type datetime.now()
    - **friends**: list of friends, type List[Friend] (model of data Friends)
    - **is_active**: by default is True, type bool
    - **is_superuser**: by default is False, type bool
    - **is_verified**: by default is False, type bool
    """
    try:
        result = await User.find_one(User.username == new_user.username)
        if result:
            return {
                "message": "Username already registered. Please, change username."}
        else:
            check_password = await pass_validation(new_user.hashed_password)
            if check_password:
                return {"message": check_password}
            new_user.hashed_password = await hash_password(new_user.hashed_password)
            result = await User.insert(new_user)
            return {"message": "New user created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# get user info by username
@auth_router.get("/user/{username}", summary='Get user info')
async def get_user(username: str):
    """
    - **username**: username of a user
    """
    try:
        result = await User.find_one({"username": username}).project(ReadUser)
        if result:
            return result
        else:
            return {"message": "Error 404: No user found."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
