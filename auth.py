# app/auth.py
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from pwdlib import PasswordHash

from database import get_session
from models.user import User, RoleEnum

SECRET = "SECRETKEY"
ALGO = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
password_hash = PasswordHash.recommended()



def hash_password(pwd_text: str):
    return password_hash.hash(pwd_text)


def verify_password(password: str, hashed: str):
    return password_hash.verify(password, hashed)


def create_token(data: dict):
    to_encode = data.copy()
    to_encode["exp"] = datetime.now() + timedelta(hours=5)
    return jwt.encode(to_encode, SECRET, ALGO)


def authenticate_user(session: Session, username: str, password: str):
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    try:
        payload = jwt.decode(token, SECRET, [ALGO])
        username = payload.get("sub")
    except JWTError:
        raise HTTPException(401, "Invalid token")

    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(401, "User not found")
    return user


def role_required(roles: list[str]):
    def wrapper(user: User = Depends(get_current_user)):
        if user.role.value not in roles:
            raise HTTPException(403, "Not allowed")
        return user
    return wrapper
