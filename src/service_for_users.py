import re


def check_username(username):
    return bool(re.search(r"[~!@#$%^&*()+=`\-/\s]", username))
