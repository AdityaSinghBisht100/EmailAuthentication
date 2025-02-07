# app/crud.py
from app.database import DatabaseConnection
from app.models import User
from app.auth import hash_password, create_verification_token
from app.email_service import EmailService
from datetime import datetime
from app import auth

class UserService:
    @staticmethod
    async def create_user(user_data: dict):
        db = DatabaseConnection.db
        
        # Check if user already exists
        existing_user = await db.users.find_one({"email": user_data['email']})
        if existing_user:
            return None
        
        # Prepare user data
        verification_token = create_verification_token()
        hashed_password = hash_password(user_data['password'])
        
        # Create user document
        user_doc = {
            "email": user_data['email'],
            "hashed_password": hashed_password,
            "verification_token": verification_token,
            "is_active": False,
            "created_at": datetime.utcnow()
        }
        
        # Insert user
        result = await db.users.insert_one(user_doc)
        
        # Send verification email
        email_sent = EmailService.send_verification_email(
            user_data['email'], 
            verification_token
        )
        
        # Return result
        return {
            "user_id": str(result.inserted_id),
            "email_sent": email_sent
        }
    @staticmethod
    async def authenticate_user(email: str, password: str):
        db = DatabaseConnection.db
        user = await db.users.find_one({"email": email})
        
        if not user:
            return None
        
        # Check password and account activation
        if not auth.verify_password(password, user['hashed_password']):
            return None
        
        if not user.get('is_active', False):
            return None
        
        return user

    @staticmethod
    async def verify_user(token: str):
        db = DatabaseConnection.db
        user = await db.users.find_one({"verification_token": token})
        
        if not user:
            return False
        
        # Update user to mark as verified
        result = await db.users.update_one(
            {"verification_token": token},
            {"$set": {
                "is_active": True, 
                "verification_token": None
            }}
        )
        
        return result