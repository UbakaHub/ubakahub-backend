from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class PersonalInfo(BaseModel):
    full_name: Optional[str]
    phone: Optional[str]

class LandInfo(BaseModel):
    plot_number: Optional[str]
    district: Optional[str]
    sector: Optional[str]
    cell: Optional[str]

class User(BaseModel):
    id: Optional[str] = Field(alias="_id")
    email: EmailStr
    hashed_password: str
    personal_info: Optional[PersonalInfo] = None
    land_info: Optional[LandInfo] = None
    is_active: bool = True