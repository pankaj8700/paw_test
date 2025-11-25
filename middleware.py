# app/middleware.py
import time
from fastapi import Request
from fastapi.responses import Response


async def custom_middleware(request: Request, call_next):
    start = time.time()

    response = await call_next(request)

    duration = time.time() - start

    response.headers["X-Process-Time"] = str(round(duration, 4))
    response.headers["X-App"] = "RBAC-SQLModel"

    return response
