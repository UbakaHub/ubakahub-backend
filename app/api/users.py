from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, PersonalInfoSchema, LandInfoSchema
from app.services.user_services import create_user, validate_user, get_user_by_email
from app.auth.jwt_handler import create_token
from app.auth.deps import get_current_user
from app.models.user import User
from app.db import get_user_collection
from passlib.hash import bcrypt

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/signup")
def signup(user: UserCreate):
    users = get_user_collection()
    if users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = bcrypt.hash(user.password)
    new_user = {
        "email": user.email,
        "hashed_password": hashed_pw,
        "personal_info": None,
        "land_info": None
    }
    users.insert_one(new_user)
    return {"message": "User created!"}

@router.post("/{email}/personal-info")
def update_personal_info(email: str, info: PersonalInfoSchema):
    users = get_user_collection()
    result = users.update_one({"email": email}, {"$set": {"personal_info": info.dict()}})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Personal info updated!"}

@router.post("/{email}/land-info")
def update_land_info(email: str, info: LandInfoSchema):
    users = get_user_collection()
    result = users.update_one({"email": email}, {"$set": {"land_info": info.dict()}})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Land info updated!"}
