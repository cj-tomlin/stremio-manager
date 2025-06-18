from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from app.database import engine
from app.api.v1.routers import user_router, auth_router, addon_router

app = FastAPI(
    title="Stremio Manager API",
    description="Manages Stremio, Trakt, and Debrid integration for users.",
    version="0.1.0",
)

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables() # Alembic now handles table creation

app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(addon_router.router, prefix="/api/v1", tags=["addons"])
app.include_router(user_router.router, prefix="/api/v1/users", tags=["users"])

@app.get("/")
async def root():
    return {"message": "Welcome to Stremio Manager API"}


