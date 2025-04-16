# app/utils/email.py
import smtplib
import sib_api_v3_sdk
from email.message import EmailMessage
from sib_api_v3_sdk.rest import ApiException
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("BREVO_API_KEY")
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = api_key
api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

def send_welcome_email(to_email: str):
    subject = "Welcome to UbakaHub 👷🏾‍♀️"
    sender = {"name": "UbakaHub", "email": "no-reply@ubakahub.rw"}  # use domain email if you have one
    to = [{"email": to_email}]
    html_content = """
    <html>
    <body>
        <h2>Welcome to UbakaHub 👷🏾‍♀️</h2>
        <p>We’re thrilled to have you join our building revolution! 🏗️</p>
        <p>Stay tuned for exciting updates as we launch tools for builders across Rwanda.</p>
        <p>Thanks for believing in our mission.</p>
        <br>
        <p>– Bwiza & the UbakaHub Team</p>
    </body>
    </html>
    """
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,
        sender=sender,
        subject=subject,
        html_content=html_content,
        tags=["early access"]
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(f"Email sent: {api_response}")
    except ApiException as e:
        print(f"Error sending email: {e}")