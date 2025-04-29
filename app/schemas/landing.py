from pydantic import BaseModel, EmailStr

class InterestSignup(BaseModel):
    email: EmailStr