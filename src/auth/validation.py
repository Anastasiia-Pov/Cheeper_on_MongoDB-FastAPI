from fastapi import HTTPException, status, Response, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from models.user_models import UserSchema
from models.jwt_token import TokenInfo
from auth import utils_jwt as auth_utils
from routers.friends import check_user_existence
from auth.helpers import (TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE,
                          REFRESH_TOKEN_TYPE)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth-jwt/login")


def validate_token_type(payload: dict,
                        token_type: str) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if payload.get(TOKEN_TYPE_FIELD) == token_type:
        return True
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"invalid token type {current_token_type!r} expected '{token_type}'.")


def get_current_token_payload(
        token: str = Depends(oauth2_scheme)
        ) -> dict:
    try:
        payload = auth_utils.decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Invalid token error: {e}")
    return payload


async def get_user_by_token(payload: dict) -> UserSchema:
    username: str | None = payload.get("username")
    if user := await check_user_existence(username):
        return user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Token invalid (user not found).")


def get_auth_user_from_token_of_type(token_type: str):
    async def get_auth_user_from_token(payload: dict = Depends(get_current_token_payload)) -> UserSchema:
        validate_token_type(payload, token_type)
        return await get_user_by_token(payload)
    return get_auth_user_from_token


# class UserGetterFromToken:
#     def __init__(self, token_type: str):
#         self.token_type = token_type

#     def __call__(self,
#                  payload: dict = Depends(get_current_token_payload),
#                  ):
#         validate_token_type(payload, self.token_type)
#         return get_user_by_token(payload)


get_current_auth_user = get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = get_auth_user_from_token_of_type(REFRESH_TOKEN_TYPE)
