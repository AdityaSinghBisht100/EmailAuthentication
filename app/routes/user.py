from fastapi import APIRouter, HTTPException, Depends
from app.controllers.controller import create_user, authenticate_user, verify_user, get_current_user
from app.services.auth import create_access_token
from fastapi import status,Response

user_router = APIRouter()

@user_router.get("/user")
async def get_user(current_user: dict = Depends(get_current_user)):
    print(current_user)
    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    return {"email": current_user["email"]}

@user_router.post("/signup")
async def signup(user_data: dict):
    result = await create_user(user_data)
    
    if not result:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    if not result.get('email_sent'):
        raise HTTPException(
            status_code=500, 
            detail="User created but verification email failed"
        )
    print(result)
    return {
        "message": "User registered. Check email for verification.",
        "user_id": result['user_id']
    }

@user_router.get("/verify")
async def verify_email(token: str):
    success = await verify_user(token)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid or already verified token")
    
    return {"message": "Email verified successfully"}

@user_router.post("/login")
async def login(user_data: dict,res: Response):
    user = await authenticate_user(
        user_data['email'], 
        user_data['password']
    )
    
    if not user:
        raise HTTPException(
            status_code=401, 
            detail="Invalid credentials or unverified account"
        )
    
    access_token = create_access_token({"sub": user['email']});
    res.status_code = status.HTTP_200_OK
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }