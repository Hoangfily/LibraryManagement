from fastapi import FastAPI

from app.modules.auth.router import router as auth_router
from app.modules.borrows.router import router as borrows_router
from app.modules.copies.router import router as copies_router
from app.modules.documents.router import router as documents_router
from app.modules.fines.router import router as fines_router
from app.modules.readers.router import router as readers_router
from app.modules.reports.router import router as reports_router
from app.modules.users.router import router as users_router

# Entry point cua ung dung FastAPI.
app = FastAPI(title="Library Management API")

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
    # Endpoint kiem tra server dang chay.
    return {"message": "Library Management API"}
