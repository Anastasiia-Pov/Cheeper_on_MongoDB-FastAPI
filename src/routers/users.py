import logging
from service.service_for_password import hash_password, pass_validation
from service.service_for_users import check_username
from models.user_models import User, ReadUser
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
        if check_username(new_user.username):
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"message": "Username can't include spaces or special symbols"}
        else:
            check_password = pass_validation(new_user.hashed_password)
            if check_password:
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {"message": check_password}
            new_user.hashed_password = hash_password(new_user.hashed_password)
            result = await User.insert(new_user)
            return {"message": "New user created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# get user info by username
@auth_router.get("/user/{username}", summary='Get user info')
async def get_user(username: str,
                   response: Response):
    try:
        user = await User.find_one({"username": username})
        if user:
            if user.is_active:
                return user
            response.status_code = status.HTTP_403_FORBIDDEN
            return {"message": "User is inactive."}
        return {"message": "User inactive"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# get user info by username
@auth_router.delete("/user/{id}",
                    status_code=status.HTTP_200_OK,
                    summary='Delete user')
async def delete_user(id: str,
                      response: Response):
    try:
        result = await User.get(id)
        if result:
            await result.delete()
            return {"message": "User deleted successfully"}
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "No user found."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
