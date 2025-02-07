from app.db.database import DatabaseConnection
from app.models.models import User
from app.services.auth import hash_password, verify_password, create_verification_token
from app.services.email_service import send_verification_email
from datetime import datetime

async def create_user(user_data: dict):
    db = DatabaseConnection.db
    existing_user = await db.users.find_one({"email": user_data['email']})
    if existing_user:
        return None

    verification_token = create_verification_token()
    hashed_password = hash_password(user_data['password'])

    user_doc = {
        "email": user_data['email'],
        "hashed_password": hashed_password,
        "verification_token": verification_token,
        "is_active": False,
        "created_at": datetime.utcnow()
    }

    result = await db.users.insert_one(user_doc)
    email_sent = send_verification_email(user_data['email'], verification_token)

    return {
        "user_id": str(result.inserted_id),
        "email_sent": email_sent
    }

async def authenticate_user(email: str, password: str):
    db = DatabaseConnection.db
    user = await db.users.find_one({"email": email})
    
    if not user or not verify_password(password, user['hashed_password']) or not user.get('is_active', False):
        return None

    return user

async def verify_user(token: str):
    db = DatabaseConnection.db
    user = await db.users.find_one({"verification_token": token})
    
    if not user:
        return False

    result = await db.users.update_one(
        {"verification_token": token},
        {"$set": {
            "is_active": True, 
            "verification_token": None
        }}
    )

    return result
