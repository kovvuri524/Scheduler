"""
Email Handler

Purpose:
--------
Sends email notifications for scan events.

Responsibilities:
-----------------
1. Send Scan Started notifications.
2. Send Scan Completed notifications.
3. Send Scan Failed notifications.
4. Send Duplicate Scan notifications.

SMTP Server:
------------
Gmail SMTP (smtp.gmail.com)

Authentication:
---------------
Uses Gmail App Password authentication.

Used By:
--------
- start_handler.py
- end_handler.py
- scheduler.py
"""

"""
Email Handler
"""



import os
import smtplib

from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


async def send_email(
    subject,
    body
):

    sender_email = os.getenv(
        "EMAIL_ID"
    )

    sender_password = os.getenv(
        "EMAIL_PASSWORD"
    )

    recipient_email = os.getenv(
        "RECIPIENT_EMAIL"
    )

    msg = EmailMessage()

    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    msg.set_content(body)

    with smtplib.SMTP(
        "smtp.gmail.com",
        587
    ) as server:

        server.starttls()

        server.login(
            sender_email,
            sender_password
        )

        server.send_message(msg)
