from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token_hash = Column(String(255), nullable=False, index=True)
    otp_hash = Column(String(255), nullable=True)
    staged_password_hash = Column(String(255), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    otp_expires_at = Column(DateTime(timezone=True), nullable=True)
    otp_attempts = Column(Integer, default=0, nullable=False)
    otp_verified = Column(Boolean, default=False, nullable=False)
    used = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", backref="password_reset_requests")

    def __repr__(self):
        return f"<PasswordResetToken(id={self.id}, user_id={self.user_id}, verified={self.otp_verified}, used={self.used})>"
