from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import Session, select

from database import create_db_and_tables, engine
from models.user import User, RoleEnum
from auth import hash_password
from middleware import custom_middleware

from routers import auth, users, tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 App starting...")
    create_db_and_tables()

    # Create default admin
    with Session(engine) as session:
        existing = session.exec(select(User).where(User.username == "admin")).first()

        if not existing:
            admin = User(
                username="admin",
                hashed_password=hash_password("Test_123"),
                role=RoleEnum.admin
            )
            session.add(admin)
            session.commit()
            print("✓ Default admin created")
    yield
    print("🛑 App shutdown...")


app = FastAPI(title="FastAPI Modular RBAC", lifespan=lifespan)

# Middleware
app.middleware("http")(custom_middleware)

# Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)
