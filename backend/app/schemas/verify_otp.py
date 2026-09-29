from pydantic import BaseModel, Field

class VerifyOTPRequest(BaseModel):
    reset_token: str = Field(..., json_schema_extra={"example": "abc123token"})
    otp: str = Field(..., min_length=6, max_length=6, json_schema_extra={"example": "123456"})

class VerifyOTPResponse(BaseModel):
    message: str
    otp_verified: bool = True
