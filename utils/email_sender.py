import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()
app_password = os.getenv("APP_PASSWORD")
sender_email = os.getenv("SENDER_EMAIL")


def send_email(reciever_email: str,subject: str,content: str)->str:
    """
    send an email to the reciever_email with the subject and content
    """

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = reciever_email
    msg["Subject"] = subject
    msg.set_content(content)

    # Connect to Gmail Server
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)



    print("Email sent successfully")

if __name__ == "__main__":
    send_email("4mh23cs179@gmail.com", subject="Hello from python",content="this is a test emailfrom python")
