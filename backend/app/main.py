from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.db.database import engine, Base, get_db
from app.models.user import User
from app.models.password_reset import PasswordResetToken
from app.routes import auth, password_reset

# Bind tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Secure Password Reset & OTP Auth API",
    description="A production-ready FastAPI backend with JWT auth and OTP password reset.",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(password_reset.router)

@app.get("/", tags=["Health Check"])
def read_root():
    return {
        "status": "online",
        "message": "Welcome to the Secure Password Reset & OTP Authentication API"
    }

@app.get("/db-test", tags=["Health Check"])
def db_test(db: Session = Depends(get_db)):
    user_count = db.query(User).count()
    reset_count = db.query(PasswordResetToken).count()
    return {
        "database_status": "connected",
        "total_users": user_count,
        "total_reset_requests": reset_count
    }
