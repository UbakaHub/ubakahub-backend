from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import users, interest


app=FastAPI(title="UbakaHub API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #We'll update later for security
    # allow_origins=["http://localhost:3000", "https://your-production-domain.com"],
    # allow_origins=["http://localhost:3000"], # For local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(interest.router)
# Include other routers here as needed

@app.get("/")
def root():
    return {"message": "Welcome to the UbakaHub backend!"}
