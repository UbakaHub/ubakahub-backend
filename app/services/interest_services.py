from app.db import get_interest_collection
from app.utils.email import send_welcome_email
from datetime import datetime, timezone

def save_interest_email(email: str):
    collection = get_interest_collection()
    if collection.find_one({"email": email}):
        return False  # Already exists
    
    collection.insert_one({
        "email": email,
        "created_at": datetime.now(timezone.utc),
        "welcome_sent": False
    })

    try:
        send_welcome_email(email)
        collection.update_one({"email": email}, {"$set": {"welcome_sent": True}})
    except Exception as e:
        print(f"Email failed: {e}")

    return True