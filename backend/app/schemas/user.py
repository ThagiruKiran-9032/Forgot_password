from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
import re

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, json_schema_extra={"example": "Kittu"})
    email: EmailStr = Field(..., json_schema_extra={"example": "kittu@example.com"})
    password: str = Field(..., min_length=8, json_schema_extra={"example": "Password@123"})

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character.")
        return value

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
