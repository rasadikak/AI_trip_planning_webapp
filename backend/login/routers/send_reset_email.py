from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from backend.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,  # your email
    MAIL_PASSWORD=settings.MAIL_PASSWORD,  # your email password / app password
    MAIL_FROM=settings.MAIL_FROM,          # sender email
    MAIL_PORT=settings.MAIL_PORT,          # port number (587 or 465)
    MAIL_SERVER=settings.MAIL_SERVER,      # smtp.gmail.com, etc.
    MAIL_TLS=settings.MAIL_TLS,            # True or False
    MAIL_SSL=settings.MAIL_SSL,            # True or False
    USE_CREDENTIALS=True                    # login required
)

async def send_reset_email(email: str, link: str):
    message = MessageSchema(
        subject="Reset Your Password",
        recipients=[email],
        body=f"""
        Click this link to reset your password:

        {link}

        This link expires in 15 minutes.
        """,
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)