# routes/user.py
from fastapi import APIRouter, HTTPException
from app.crud import UserService
from app.auth import create_access_token


user_router = APIRouter()

@user_router.post("/signup")
async def signup(user_data: dict):
    result = await UserService.create_user(user_data)
    
    if not result:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    if not result.get('email_sent'):
        raise HTTPException(
            status_code=500, 
            detail="User created but verification email failed"
        )
    
    return {
        "message": "User registered. Check email for verification.",
        "user_id": result['user_id']
    }

@user_router.get("/verify")
async def verify_email(token: str):
    result = await UserService.verify_user(token)
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Invalid verification token")
    return {"message": "Email verified successfully"}

@user_router.post("/login")
async def login(user_data: dict):
    user = await UserService.authenticate_user(
        user_data['email'], 
        user_data['password']
    )
    
    if not user:
        raise HTTPException(
            status_code=401, 
            detail="Invalid credentials or unverified account"
        )
    
    access_token = create_access_token({"sub": user['email']})
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }