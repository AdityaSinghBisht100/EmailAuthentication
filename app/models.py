from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

class User(BaseModel):
    id: Optional[PyObjectId] = None
    email: EmailStr
    hashed_password: str
    is_active: bool = False
    verification_token: Optional[str] = None
    created_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}