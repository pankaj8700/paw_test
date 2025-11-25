from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from schemas.user import UserCreate, UserRead
from models.user import User
from auth import hash_password, role_required

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserRead,
            description="role can be only admin, manager, employee")
def create_user(
    user_in: UserCreate,
    session: Session = Depends(get_session),
    _: User = Depends(role_required(["admin"]))
):
    existing = session.exec(select(User).where(User.username == user_in.username)).first()
    if existing:
        raise HTTPException(400, "Username already exists")

    user = User(
        username=user_in.username,
        hashed_password=hash_password(user_in.password),
        role=user_in.role
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/", response_model=list[UserRead])
def list_users(
    session: Session = Depends(get_session),
    _: User = Depends(role_required(["admin"]))
):
    return session.exec(select(User)).all()
