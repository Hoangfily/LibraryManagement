"""
Entry point for the FastAPI application.
On startup: creates all database tables and seeds the default admin account.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    Lifespan event handler: runs on app startup and shutdown.
    - Creates all database tables (if they don't exist).
    - Seeds the default admin account.
    """
    # Startup
    init_db()
    db = SessionLocal()
    try:
        seed_admin(db)
    finally:
        db.close()
    yield
    # Shutdown (nothing to do)


app = FastAPI(title="Library Management API", lifespan=lifespan)

# CORS — allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers for each module for easy task splitting and code merging.
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
    """Health check endpoint to verify the server is running."""
    return {"message": "Library Management API"}
