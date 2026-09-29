import secrets
import hashlib

def generate_secure_otp() -> str:
    """Generate a cryptographically secure 6-digit OTP string."""
    otp_number = secrets.randbelow(900000) + 100000
    return f"{otp_number:06d}"

def generate_secure_token() -> str:
    """Generate a cryptographically secure URL-safe random string for reset token."""
    return secrets.token_urlsafe(32)

def hash_secret(value: str) -> str:
    """Hash a secret string (reset token or OTP) using SHA-256."""
    return hashlib.sha256(value.encode("utf-8")).hexdigest()
