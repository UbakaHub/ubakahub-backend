from app.db import get_user_collection
from app.auth.security import hash_password, verify_password

def get_user_by_email(email: str):
    return get_user_collection().find_one({"email": email})

def create_user(email: str, password: str):
    user = {
        "email": email,
        "hashed_password": hash_password(password),
        "personal_info": None,
        "land_info": None
    }
    get_user_collection().insert_one(user)
    return user

def validate_user(email: str, password: str):
    user = get_user_by_email(email)
    if user and verify_password(password, user["hashed_password"]):
        return user
    return None
