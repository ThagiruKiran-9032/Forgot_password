from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.schemas.login import LoginRequest, TokenResponse
from app.services.auth_service import register_user, login_user
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Registers a new user with email, name, and password. Hashes the password before storing."
)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    return register_user(db=db, user_in=user_in)

@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="User login",
    description="Authenticates user credentials and returns a signed JWT access token."
)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    return login_user(db=db, credentials=credentials)

@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user profile",
    description="Protected route. Returns profile information of the currently logged-in user extracted from JWT."
)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
