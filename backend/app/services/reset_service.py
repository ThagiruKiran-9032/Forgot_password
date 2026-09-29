from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.models.password_reset import PasswordResetToken
from app.utils.otp import generate_secure_token, generate_secure_otp, hash_secret
from app.utils.password import hash_password
from app.schemas.verify_otp import VerifyOTPRequest
from app.schemas.reset_password import ResetPasswordRequest
from app.services.email_service import send_reset_link_email, send_confirmation_otp_email
from app.core.config import settings

def request_password_reset_by_email(db: Session, email: str) -> dict:
    """
    Step 1: User submits registered email.
    Sends Password Reset Link to that email address.
    """
    now = datetime.now(timezone.utc)
    user = db.query(User).filter(User.email == email.lower()).first()

    # Prevent email enumeration attacks: if user not found, return generic success
    if not user or not user.is_active:
        return {
            "message": "If your email is registered in our system, you will receive password reset instructions."
        }

    # Enforce 60-second resend cooldown
    latest_request = db.query(PasswordResetToken).filter(
        PasswordResetToken.user_id == user.id
    ).order_by(PasswordResetToken.id.desc()).first()

    if latest_request and latest_request.created_at:
        created_at_utc = latest_request.created_at
        if created_at_utc.tzinfo is None:
            created_at_utc = created_at_utc.replace(tzinfo=timezone.utc)

        elapsed = (now - created_at_utc).total_seconds()
        COOLDOWN_SECONDS = 60
        if elapsed < COOLDOWN_SECONDS:
            remaining_seconds = max(1, int(COOLDOWN_SECONDS - elapsed))
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Please wait {remaining_seconds} second(s) before requesting another password reset."
            )

    # Invalidate older unused reset requests for this user
    db.query(PasswordResetToken).filter(
        PasswordResetToken.user_id == user.id,
        PasswordResetToken.used == False
    ).update({"used": True})

    # Generate raw secure reset token
    raw_reset_token = generate_secure_token()
    token_hash = hash_secret(raw_reset_token)

    # Set expiration timestamp (15 minutes)
    token_expires_at = now + timedelta(minutes=settings.RESET_TOKEN_EXPIRE_MINUTES)

    # Create record in PostgreSQL
    reset_record = PasswordResetToken(
        user_id=user.id,
        token_hash=token_hash,
        otp_hash=None,
        staged_password_hash=None,
        expires_at=token_expires_at,
        otp_expires_at=None,
        otp_attempts=0,
        otp_verified=False,
        used=False
    )
    db.add(reset_record)
    db.commit()

    # Send reset link email to registered email
    send_reset_link_email(
        recipient_email=user.email,
        recipient_name=user.name,
        reset_token=raw_reset_token
    )

    return {
        "message": "Password reset instructions have been sent to your registered email."
    }

def stage_new_password_and_send_otp(db: Session, data: ResetPasswordRequest) -> dict:
    """
    Step 2: User opens reset link and enters new password.
    Hashes new password, generates 6-digit OTP, and sends Confirmation OTP to user's registered email.
    """
    token_hash = hash_secret(data.reset_token)
    record = db.query(PasswordResetToken).filter(
        PasswordResetToken.token_hash == token_hash
    ).first()

    if not record or record.used:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token."
        )

    now = datetime.now(timezone.utc)
    expires_at = record.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if now > expires_at:
        record.used = True
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token has expired. Please request a new password reset."
        )

    # Hash candidate new password securely with bcrypt and stage it
    staged_pwd_hash = hash_password(data.new_password)
    record.staged_password_hash = staged_pwd_hash

    # Generate 6-digit OTP
    raw_otp = generate_secure_otp()
    record.otp_hash = hash_secret(raw_otp)
    record.otp_expires_at = now + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)
    record.otp_attempts = 0

    db.commit()

    # Query associated user
    user = db.query(User).filter(User.id == record.user_id).first()

    # Dispatch confirmation OTP email
    send_confirmation_otp_email(
        recipient_email=user.email,
        recipient_name=user.name,
        otp=raw_otp
    )

    return {
        "message": f"Confirmation OTP has been sent to your registered email ({user.email}). Please enter the 6-digit OTP to finalize your password reset.",
        "otp_required": True
    }

def confirm_otp_and_finalize_password(db: Session, data: VerifyOTPRequest) -> dict:
    """
    Step 3: User submits the 6-digit OTP.
    Verifies OTP hash. On success, updates user's password in PostgreSQL and invalidates token.
    """
    token_hash = hash_secret(data.reset_token)
    record = db.query(PasswordResetToken).filter(
        PasswordResetToken.token_hash == token_hash
    ).first()

    if not record or record.used:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token."
        )

    if not record.staged_password_hash:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please submit your new password first before verifying OTP."
        )

    now = datetime.now(timezone.utc)
    expires_at = record.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if now > expires_at:
        record.used = True
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token has expired. Please request a new password reset."
        )

    # Enforce MAX 3 attempts
    MAX_ATTEMPTS = 3
    if record.otp_attempts >= MAX_ATTEMPTS:
        record.used = True
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum OTP verification attempts exceeded. Reset request has been invalidated."
        )

    otp_expires_at = record.otp_expires_at
    if otp_expires_at and otp_expires_at.tzinfo is None:
        otp_expires_at = otp_expires_at.replace(tzinfo=timezone.utc)

    if otp_expires_at and now > otp_expires_at:
        record.otp_attempts += 1
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP has expired. Please request a new password reset."
        )

    # Compare OTP hash
    incoming_otp_hash = hash_secret(data.otp)
    if incoming_otp_hash != record.otp_hash:
        record.otp_attempts += 1
        remaining = MAX_ATTEMPTS - record.otp_attempts
        if record.otp_attempts >= MAX_ATTEMPTS:
            record.used = True
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Maximum OTP verification attempts exceeded. Reset request has been invalidated."
            )
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid OTP code. {remaining} attempt(s) remaining."
        )

    # SUCCESS: Finalize password change in PostgreSQL users table!
    user = db.query(User).filter(User.id == record.user_id).first()
    user.password_hash = record.staged_password_hash

    # Invalidate reset request
    db.query(PasswordResetToken).filter(
        PasswordResetToken.user_id == user.id
    ).update({"used": True})

    record.otp_verified = True
    db.commit()

    return {
        "message": "Password reset confirmed and completed successfully! You can now log in with your new password.",
        "success": True
    }
