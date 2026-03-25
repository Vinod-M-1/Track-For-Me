import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

load_dotenv()

EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")


def send_email(to_email, product_name, price):
    subject = "Price Drop Alert!"
    body = f"{product_name} is now at {price}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL
    msg['To'] = to_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL, APP_PASSWORD)
            server.send_message(msg)

        print("Email sent!")

    except Exception as e:
        print("Email error:", e)