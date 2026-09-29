from pydantic import BaseModel, EmailStr, Field

class ForgotPasswordRequest(BaseModel):
    email: EmailStr = Field(..., json_schema_extra={"example": "kittu@example.com"})

class ForgotPasswordResponse(BaseModel):
    message: str
