from celery import Celery
from .database import get_db
from .models import Switch
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize the Celery app
celery = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)

celery.conf.beat_schedule = {
    "check-switches-every-minute": {
        "task": "app.tasks.check_switches",
        "schedule": 30.0,
    },
}

celery.conf.timezone = "UTC"


@celery.task
def check_switches():
    print("Checking switches...")

    try:
        # Create a new database session
        db = next(get_db())

        # Get current time in UTC
        now = datetime.utcnow()
        seven_days_from_now = now + timedelta(days=7)

        # Get switches from database
        db_switches = db.query(Switch).all()

        for switch in db_switches:
            print(f"Switch: {switch.id} - {switch.name} - {switch.expiration_datetime}")
            
            # Check if expiration is less than 7 days away
            if switch.expiration_datetime and switch.expiration_datetime <= seven_days_from_now:
                # Send email notification
                send_expiration_email(switch.user_email, switch.name, switch.expiration_datetime)

        # Make sure to close the session
        db.close()

    except Exception as e:
        print(f"Error getting switches: {e}")
        return

def send_expiration_email(recipient_email: str, switch_name: str, expiration_date: datetime):
    # Email configuration
    smtp_server = os.getenv("MAIL_SERVER")
    smtp_port = int(os.getenv("MAIL_PORT", 587))
    sender_email = os.getenv("MAIL_FROM")
    password = os.getenv("MAIL_PASSWORD")

    # Create message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Switch Expiration Warning"

    # Create the email body
    body = f"""
    <html>
        <body>
            <p>Your switch '{switch_name}' will expire on {expiration_date.strftime('%Y-%m-%d')}.</p>
            <p>Please take necessary action.</p>
        </body>
    </html>
    """
    
    # Add body to email
    message.attach(MIMEText(body, "html"))

    try:
        # Create SMTP session with proper connection sequence
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()  # Identify ourselves to the SMTP server
            server.starttls()  # Start TLS encryption
            server.ehlo()  # Re-identify ourselves over TLS connection
            server.login(sender_email, password)
            text = message.as_string()
            server.sendmail(sender_email, recipient_email, text)
            print(f"Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
