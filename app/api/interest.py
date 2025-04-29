from fastapi import APIRouter, HTTPException
from app.schemas.landing import InterestSignup
from app.services.interest_services import save_interest_email

router = APIRouter(prefix="/landing", tags=["Landing Page"])

@router.post("/signup")
def collect_interest(signup: InterestSignup):
    success = save_interest_email(signup.email)
    if not success:
        raise HTTPException(status_code=400, detail="You've already signed up!")
    return {"message": "Thank you! We'll keep you updated 🚀"}
