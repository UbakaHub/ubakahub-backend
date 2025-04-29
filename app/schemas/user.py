from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class PersonalInfoSchema(BaseModel):
    full_name: Optional[str]
    phone: Optional[str]

class LandInfoSchema(BaseModel):
    plot_number: Optional[str]
    district: Optional[str]
    sector: Optional[str]
    cell: Optional[str]
