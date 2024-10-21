from fastapi import APIRouter, status, Depends
from fastapi.security import HTTPBearer
from models.user_models import UserSchema
from models.jwt_token import TokenInfo
from auth.helpers import create_access_token, create_refresh_token
from auth.validation import (get_current_auth_user_for_refresh,
                             validate_auth_user,
                             get_current_token_payload,
                             get_current_active_auth_user)

http_bearer = HTTPBearer(auto_error=False)


jwt_router = APIRouter(prefix="/auth-jwt",
                       tags=["Auth-JWT"],
                       dependencies=[Depends(http_bearer)])


@jwt_router.post("/login",
                 status_code=status.HTTP_200_OK,
                 summary='Authentification',
                 response_model=TokenInfo)
async def auth_user_jwt(user: UserSchema = Depends(validate_auth_user)):
    access_token = await create_access_token(user)
    refresh_token = await create_refresh_token(user)
    return TokenInfo(access_token=access_token,
                     refresh_token=refresh_token)


@jwt_router.post("/refresh/",
                 response_model=TokenInfo,
                 response_model_exclude_none=True)
async def auth_refresh_jwt(user: UserSchema = Depends(get_current_auth_user_for_refresh)):
    access_token = await create_access_token(user)
    return TokenInfo(
        access_token=access_token
    )


@jwt_router.get("/users/me",
                status_code=status.HTTP_200_OK,
                summary='Get user')
async def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserSchema = Depends(get_current_active_auth_user)
):
    iat = payload.get('iat')
    return {"username": user.username,
            "email": user.email,
            "logged_in_at": iat}
