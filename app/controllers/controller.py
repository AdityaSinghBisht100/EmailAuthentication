from app.db.database import DatabaseConnection
from app.models.models import User
from app.services.auth import hash_password, verify_password, create_verification_token
from app.services.email_service import send_verification_email
from datetime import datetime
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends
from app.services.auth import decode_access_token
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

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
    
    if not user or not verify_password(password, user['hashed_password']):
        return None

    return user

async def verify_user(token: str) -> bool:
    if not token:
        logger.error("No token provided for verification")
        return False

    db = DatabaseConnection.db
    result = await db.users.update_one(
        {"verification_token": token, "is_active": False}, 
        {"$set": {"is_active": True, "verification_token": None}}
    )
    if result.modified_count == 0:
        logger.warning(f"Invalid or already verified token: {token}")
        return False

    logger.info(f"User successfully verified with token: {token}")
    return True


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return {"email": payload["sub"]}