import hashlib
import re


async def hash_password(password):
   password_bytes = password.encode('utf-8')
   hash_object = hashlib.sha256(password_bytes)
   return hash_object.hexdigest()


async def pass_validation(password):
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

    if not any(re.findall(r'[~!@#$%^&\*()_+=-`]', password)):
        errors.append("Password should have at least one of the symbols: ~, !, @, #, $, %, ^, &, *, (, ), _, +, =, -,")
        validation = False

    if not validation:
        return errors
