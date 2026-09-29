import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

def send_reset_link_email(recipient_email: str, recipient_name: str, reset_token: str) -> bool:
    """
    Step 1 Email Dispatch:
    Sends Password Reset Link to the user's registered email address.
    """
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
    subject = "Password Reset Link Request"

    body_text = f"""Hello {recipient_name},

We received a request to reset your password.

Reset Password Link:
{reset_url}

This reset link expires in {settings.RESET_TOKEN_EXPIRE_MINUTES} minutes.

If you did not request this, please ignore this email.
"""

    body_html = f"""<html>
  <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
    <h2 style="color: #2b6cb0;">Password Reset Request</h2>
    <p>Hello <strong>{recipient_name}</strong>,</p>
    <p>We received a request to reset your password.</p>

    <div style="background: #edf2f7; padding: 16px; border-radius: 8px; margin: 20px 0;">
      <p style="margin: 0; font-weight: bold;">Click the link below to set your new password:</p>
      <p style="margin: 12px 0;">
        <a href="{reset_url}" style="display: inline-block; padding: 10px 18px; background: #3182ce; color: #ffffff; text-decoration: none; border-radius: 6px; font-weight: bold;">Reset Password</a>
      </p>
      <p style="font-size: 13px; color: #718096; margin: 8px 0 0 0;">Link: {reset_url}</p>
    </div>

    <p style="font-size: 13px; color: #718096;">This reset link expires in {settings.RESET_TOKEN_EXPIRE_MINUTES} minutes.</p>
  </body>
</html>"""

    print(f"\n================ [EMAIL SERVICE: RESET LINK OUTBOX] ================")
    print(f"To: {recipient_email}")
    print(f"Subject: {subject}")
    print(f"Reset URL: {reset_url}")
    print(f"====================================================================\n")

    if "your_email@gmail.com" in settings.SMTP_USERNAME or "your_app_password" in settings.SMTP_PASSWORD:
        return True

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = settings.FROM_EMAIL or settings.SMTP_USERNAME
        msg["To"] = recipient_email
        msg.attach(MIMEText(body_text, "plain"))
        msg.attach(MIMEText(body_html, "html"))

        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.sendmail(msg["From"], [recipient_email], msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"[EMAIL SERVICE ERROR] {e}")
        return False

def send_confirmation_otp_email(recipient_email: str, recipient_name: str, otp: str) -> bool:
    """
    Step 2 Email Dispatch:
    Sends 6-digit Confirmation OTP after setting up new password to finalize password reset.
    """
    subject = "Password Reset Confirmation OTP"

    body_text = f"""Hello {recipient_name},

You have submitted a new password. To confirm and complete your password reset, please enter the following 6-digit OTP code:

Confirmation OTP:
{otp}

This OTP expires in {settings.OTP_EXPIRE_MINUTES} minutes.
"""

    body_html = f"""<html>
  <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
    <h2 style="color: #2b6cb0;">Confirm Password Reset</h2>
    <p>Hello <strong>{recipient_name}</strong>,</p>
    <p>You have submitted a new password. Please use the 6-digit OTP below to confirm your password change:</p>

    <div style="background: #edf2f7; padding: 16px; border-radius: 8px; margin: 20px 0; text-align: center;">
      <p style="margin: 0; font-weight: bold;">Your Confirmation OTP Code:</p>
      <h1 style="color: #2b6cb0; letter-spacing: 6px; font-size: 32px; margin: 8px 0;">{otp}</h1>
      <p style="font-size: 13px; color: #718096; margin: 0;">Expires in {settings.OTP_EXPIRE_MINUTES} minutes.</p>
    </div>
  </body>
</html>"""

    print(f"\n================ [EMAIL SERVICE: CONFIRMATION OTP OUTBOX] ================")
    print(f"To: {recipient_email}")
    print(f"Subject: {subject}")
    print(f"Confirmation OTP: {otp}")
    print(f"=========================================================================\n")

    if "your_email@gmail.com" in settings.SMTP_USERNAME or "your_app_password" in settings.SMTP_PASSWORD:
        return True

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = settings.FROM_EMAIL or settings.SMTP_USERNAME
        msg["To"] = recipient_email
        msg.attach(MIMEText(body_text, "plain"))
        msg.attach(MIMEText(body_html, "html"))

        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.sendmail(msg["From"], [recipient_email], msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"[EMAIL SERVICE ERROR] {e}")
        return False
