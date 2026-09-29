from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., json_schema_extra={"example": "kittu@example.com"})
    password: str = Field(..., json_schema_extra={"example": "Password@123"})

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_minutes: int
