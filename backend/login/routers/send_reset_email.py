from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from backend.config import settings
from fastapi import HTTPException
from backend.logger import logger

conf = ConnectionConfig(
    MAIL_USERNAME   = settings.MAIL_USERNAME,  # your email
    MAIL_PASSWORD   = settings.MAIL_PASSWORD,  # your email password / app password
    MAIL_FROM       = settings.MAIL_FROM,      # sender email
    MAIL_PORT       = settings.MAIL_PORT,      # port number (587 or 465)
    MAIL_SERVER     = settings.MAIL_SERVER,    # smtp.gmail.com, etc.
    MAIL_STARTTLS   = settings.MAIL_STARTTLS,  # True or False
    MAIL_SSL_TLS    = settings.MAIL_SSL_TLS,   # True or False
    USE_CREDENTIALS = True                     # login required
)


async def send_reset_email(email: str, link: str):
    logger.info(f"Sending password reset email — email:{email}")
    message = MessageSchema(
        subject    = "Reset Your Password",
        recipients = [email],
        body       = f"""
        Click this link to reset your password:
        {link}
        This link expires in 15 minutes.
        """,
        subtype = "plain"
    )
    fm = FastMail(conf)

    try:
        await fm.send_message(message)
        logger.info(f"Password reset email sent successfully — email:{email}")
    except Exception as e:
        logger.error(f"Failed to send reset email — email:{email} error:{e}")
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")