from fastapi import APIRouter, HTTPException, status, Response, Depends, Form
from models.user_models import UserSchema
from models.jwt_token import TokenInfo

from auth import utils_jwt as auth_utils
from service.service_for_password import validate_password
from routers.friends import check_user_existence


jwt_router = APIRouter(prefix="/auth-jwt", tags=["Auth-JWT"])


async def validate_auth_user(username: str = Form(),
                             password: str = Form()):
    unauthed_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                 detail='Invalid username or password.')
    user = await check_user_existence(username)
    if not user:
        raise unauthed_exc
    if validate_password(password=password,
                         hashed_password=user.hashed_password):
        return user
    raise unauthed_exc


@jwt_router.post("/login",
                 status_code=status.HTTP_200_OK,
                 summary='Authentification',
                 response_model=TokenInfo)
async def auth_user_jwt(user: UserSchema = Depends(validate_auth_user)):
    jwt_payload = {"username": user.username,
                   "email": user.email}
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(access_token=token,
                     token_type='Bearer')
