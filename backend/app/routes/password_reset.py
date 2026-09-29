from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.forgot_password import ForgotPasswordRequest, ForgotPasswordResponse
from app.schemas.verify_otp import VerifyOTPRequest, VerifyOTPResponse
from app.schemas.reset_password import ResetPasswordRequest
from app.services.reset_service import (
    request_password_reset_by_email,
    stage_new_password_and_send_otp,
    confirm_otp_and_finalize_password
)

router = APIRouter(prefix="/auth", tags=["Password Reset"])

@router.post(
    "/forgot-password",
    response_model=ForgotPasswordResponse,
    status_code=status.HTTP_200_OK,
    summary="Initiate password reset request by registered email",
    description="Public endpoint. Accepts registered email address and sends Password Reset Link to that email."
)
def forgot_password(
    data: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    return request_password_reset_by_email(db=db, email=data.email)

@router.post(
    "/stage-password",
    status_code=status.HTTP_200_OK,
    summary="Submit new password & dispatch confirmation OTP",
    description="Validates reset token, stages the bcrypt hashed password, and dispatches a 6-digit confirmation OTP to user's email."
)
def stage_password(
    data: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    return stage_new_password_and_send_otp(db=db, data=data)

@router.post(
    "/verify-otp",
    response_model=VerifyOTPResponse,
    status_code=status.HTTP_200_OK,
    summary="Verify confirmation OTP & finalize password reset",
    description="Verifies the 6-digit confirmation OTP, updates PostgreSQL user password_hash, and invalidates the reset token."
)
def verify_otp(
    data: VerifyOTPRequest,
    db: Session = Depends(get_db)
):
    return confirm_otp_and_finalize_password(db=db, data=data)
