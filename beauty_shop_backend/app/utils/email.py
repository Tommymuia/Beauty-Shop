import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv
import logging

# Load .env to get your Gmail credentials
load_dotenv()

# Get logger for this module
logger = logging.getLogger(__name__)

def send_invoice_email(recipient_email: str, invoice_no: str, pdf_path: str):
    """
    Send invoice email with PDF attachment.
    
    Args:
        recipient_email: Recipient's email address
        invoice_no: Invoice number
        pdf_path: Path to the PDF invoice file
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    # Validate inputs
    if not recipient_email:
        logger.error("Recipient email is None or empty")
        return False
        
    if not pdf_path or not os.path.exists(pdf_path):
        logger.error(f"PDF file not found at: {pdf_path}")
        return False
    
    # Get email configuration from environment
    mail_from = os.getenv("MAIL_FROM")
    mail_server = os.getenv("MAIL_SERVER")
    mail_port = os.getenv("MAIL_PORT")
    mail_username = os.getenv("MAIL_USERNAME")
    mail_password = os.getenv("MAIL_PASSWORD")
    
    # Validate email configuration
    if not all([mail_from, mail_server, mail_port, mail_username, mail_password]):
        logger.error("Email configuration is incomplete. Please check environment variables.")
        return False
    
    msg = EmailMessage()
    msg['Subject'] = f"Your Beauty Shop Invoice - {invoice_no}"
    msg['From'] = mail_from
    msg['To'] = recipient_email
    
    # Simple HTML Body
    html_content = f"""
    <html>
        <body>
            <h2 style="color: #d63384;">Thank you for your order!</h2>
            <p>Attached is your invoice <strong>{invoice_no}</strong>.</p>
            <p>We are preparing your package and will notify you once it's shipped.</p>
            <br>
            <p>Best Regards,<br><strong>Beauty Shop Team</strong></p>
        </body>
    </html>
    """
    msg.set_content("Please find your invoice attached.")
    msg.add_alternative(html_content, subtype='html')

    # Attach the PDF file
    try:
        with open(pdf_path, 'rb') as f:
            file_data = f.read()
            msg.add_attachment(
                file_data,
                maintype='application',
                subtype='pdf',
                filename=f"Invoice_{invoice_no}.pdf"
            )

        # Login and Send
        with smtplib.SMTP(mail_server, int(mail_port)) as smtp:
            smtp.starttls()
            smtp.login(mail_username, mail_password)
            smtp.send_message(msg)
            
        logger.info(f"Successfully sent email to {recipient_email}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"SMTP Authentication failed: {e}")
        logger.error("Please check MAIL_USERNAME and MAIL_PASSWORD in .env file")
        return False
        
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error occurred: {e}")
        return False
        
    except FileNotFoundError as e:
        logger.error(f"PDF file not found: {e}")
        return False
        
    except TypeError as e:
        if 'usedforsecurity' in str(e):
            logger.warning(f"Email sending skipped due to Python version compatibility issue: {e}")
        else:
            logger.error(f"Type error in email sending: {e}")
        return False
        
    except Exception as e:
        logger.error(f"Unexpected error sending email: {e}")
        return False