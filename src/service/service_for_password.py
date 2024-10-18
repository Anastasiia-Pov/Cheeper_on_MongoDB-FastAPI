import hashlib
import bcrypt
import re


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)
#    hash_object = hashlib.sha256(password.encode('utf-8'))
#    return hash_object.hexdigest()


def validate_password(password: str,
                      hashed_password: bytes) -> bool:
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password=password.encode(),
                          hashed_password=hashed_password)


def pass_validation(password):
    validation = True
    errors = []

    if len(password) < 8:
        errors.append('Password should have at least 8 characters')
        validation = False

    if not any(char.isdigit() for char in password):
        errors.append('Password should have at least one numeral')
        validation = False

    if not any(char.isupper() for char in password):
        errors.append('Password should have at least one uppercase letter')
        validation = False

    if not any(char.islower() for char in password):
        errors.append('Password should have at least one lowercase letter')
        validation = False

    if not any(re.findall(r'[~!@#$%^&*()_+=`\-]', password)):
        errors.append("Password should have at least one of the symbols: ~, !, @, #, $, %, ^, &, *, (, ), _, +, =, -")
        validation = False

    return errors if not validation else None
