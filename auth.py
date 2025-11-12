# auth.py
# Authentication and user management for the living web service

from datetime import datetime, timedelta
from typing import Optional
import json
import os
import uuid
from passlib.context import CryptContext
from jose import JWTError, jwt

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DATA_DIR = ".data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")

os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def create_user(email: str, password: str, username: str):
    users = load_users()
    
    # Check if email already exists
    for user in users.values():
        if user["email"] == email:
            return None, "Email already registered"
    
    user_id = str(uuid.uuid4())
    hashed_password = get_password_hash(password)
    
    user = {
        "id": user_id,
        "email": email,
        "username": username,
        "password": hashed_password,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "reputation": 0,
        "created_npcs": [],
        "remixed_content": [],
        "shared_content": []
    }
    
    users[user_id] = user
    save_users(users)
    
    # Return user without password
    safe_user = {k: v for k, v in user.items() if k != "password"}
    return safe_user, None

def authenticate_user(email: str, password: str):
    users = load_users()
    
    for user in users.values():
        if user["email"] == email:
            if verify_password(password, user["password"]):
                # Return user without password
                safe_user = {k: v for k, v in user.items() if k != "password"}
                return safe_user, None
            return None, "Invalid password"
    
    return None, "User not found"

def get_user_by_id(user_id: str):
    users = load_users()
    user = users.get(user_id)
    if user:
        # Return user without password
        safe_user = {k: v for k, v in user.items() if k != "password"}
        return safe_user
    return None

def update_user(user_id: str, updates: dict):
    users = load_users()
    if user_id in users:
        users[user_id].update(updates)
        save_users(users)
        safe_user = {k: v for k, v in users[user_id].items() if k != "password"}
        return safe_user
    return None
