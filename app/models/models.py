from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from bson import ObjectId

def validate_objectid(v):
    if not ObjectId.is_valid(v):
        raise ValueError("Invalid objectid")
    return ObjectId(v)

class User(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    hashed_password: str
    is_active: bool = False
    verification_token: Optional[str] = None
    created_at: datetime = datetime.utcnow()

    class Config:
        from_attributes = True  # Updated for Pydantic V2
        json_encoders = {ObjectId: str}
