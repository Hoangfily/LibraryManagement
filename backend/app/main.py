"""
Entry point cua ung dung FastAPI.
Khi khoi dong: tao tat ca bang trong DB va seed tai khoan admin mac dinh.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import SessionLocal, init_db
from app.modules.auth.router import router as auth_router
from app.modules.borrows.router import router as borrows_router
from app.modules.copies.router import router as copies_router
from app.modules.documents.router import router as documents_router
from app.modules.fines.router import router as fines_router
from app.modules.readers.router import router as readers_router
from app.modules.reports.router import router as reports_router
from app.modules.users.router import router as users_router
from app.modules.users.service import seed_admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event: chay khi app khoi dong va tat.
    - Tao tat ca bang trong DB (neu chua ton tai).
    - Seed tai khoan admin mac dinh.
    """
    # Startup
    init_db()
    db = SessionLocal()
    try:
        seed_admin(db)
    finally:
        db.close()
    yield
    # Shutdown (khong can lam gi)


app = FastAPI(title="Library Management API", lifespan=lifespan)

# Include cac router theo tung module de de chia viec va merge code.
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(readers_router, prefix="/readers", tags=["Readers"])
app.include_router(documents_router, prefix="/documents", tags=["Documents"])
app.include_router(copies_router, prefix="/copies", tags=["Copies"])
app.include_router(borrows_router, prefix="/borrows", tags=["Borrows"])
app.include_router(fines_router, prefix="/fines", tags=["Fines"])
app.include_router(reports_router, prefix="/reports", tags=["Reports"])


@app.get("/")
def root():
    """Endpoint kiem tra server dang chay."""
    return {"message": "Library Management API"}
