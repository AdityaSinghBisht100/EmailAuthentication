import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

def send_verification_email(email: str, verification_token: str):
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
    smtp_username = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')

    message = MIMEMultipart()
    message['From'] = smtp_username
    message['To'] = email
    message['Subject'] = 'Verify Your Account'

    verification_url = f"http://localhost:8000/users/verify?token={verification_token}"

    body = f"""
    <html>
    <body>
    <h2>Account Verification</h2>
    <p>Click the link below to verify your account:</p>
    <a href="{verification_url}">Verify Account</a>
    <p>If the link doesn't work, copy and paste this URL:</p>
    <p>{verification_url}</p>
    </body>
    </html>
    """

    message.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(message)
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False
