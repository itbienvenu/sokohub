import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

SENDER_EMAIL = os.environ.get('EMAIL_HOST_USER')
SENDER_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587


def send_email(recipient_email, subject, body_plain, sender_email=SENDER_EMAIL, sender_password=SENDER_PASSWORD, body_html=None, 
                       smtp_server="smtp.gmail.com", smtp_port=587):
    """
    Sends an email using the specified SMTP server and credentials.

    Args:
        sender_email (str): The email address of the sender.
        sender_password (str): The password or app password for the sender's account.
        recipient_email (str): The email address of the recipient.
        subject (str): The subject line of the email.
        body_plain (str): The plain text content of the email.
        body_html (str, optional): The HTML content of the email. Defaults to None.
        smtp_server (str, optional): The SMTP server address. Defaults to "smtp.gmail.com".
        smtp_port (int, optional): The SMTP server port. Defaults to 587 (TLS).
    
    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    part1 = MIMEText(body_plain, 'plain')
    msg.attach(part1)
    
    if body_html:
        part2 = MIMEText(body_html, 'html')
        msg.attach(part2)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo() # Can be omitted 
        server.starttls()  # Secure the connection
        server.ehlo() # Can be omitted 

        server.login(sender_email, sender_password)

        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        
        server.quit()
        
        return True
    
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")
        return False