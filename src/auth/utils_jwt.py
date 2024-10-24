from datetime import datetime, timedelta, timezone
from config import settings
import jwt


# >>> private_key = b"-----BEGIN PRIVATE KEY-----\nMIGEAgEAMBAGByqGSM49AgEGBS..."
# >>> public_key = b"-----BEGIN PUBLIC KEY-----\nMHYwEAYHKoZIzj0CAQYFK4EEAC..."


# Encoding JWT
def encode_jwt(payload: dict,
               private_key: str = settings.auth_jwt.private_key_path.read_text(),
               algorithm: str = settings.auth_jwt.algorithm,
               expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
               expire_timedelta: timedelta | None = None,):
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)

    delta = expire_timedelta if expire_timedelta else timedelta(minutes=expire_minutes)

    expire = now + delta

    to_encode.update(exp=expire,
                     iat=now)
    encoded = jwt.encode(to_encode,
                         private_key,
                         algorithm=algorithm,)
    return encoded


# Decoding JWT
def decode_jwt(token: str | bytes,
               public_key: str = settings.auth_jwt.public_key_path.read_text(),
               algorithm: str = settings.auth_jwt.algorithm,):
    decoded = jwt.decode(token,
                         public_key,
                         algorithms=[algorithm],
                         )
    return decoded
