from pydantic import BaseModel, Field, field_validator
import re

class ResetPasswordRequest(BaseModel):
    reset_token: str = Field(..., json_schema_extra={"example": "abc123token"})
    new_password: str = Field(..., min_length=8, json_schema_extra={"example": "NewPassword@123"})

    @field_validator("new_password")
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

class ResetPasswordResponse(BaseModel):
    message: str
