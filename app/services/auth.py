from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import secrets

ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"

def hash_password(password: str):
    return ctx.hash(password)

def verify_password(plain_password, hashed_password):
    return ctx.verify(plain_password, hashed_password)

def create_verification_token():
    return secrets.token_urlsafe(32)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
def decode_access_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload
       