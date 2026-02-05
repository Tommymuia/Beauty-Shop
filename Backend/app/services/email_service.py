import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import os

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.email = os.getenv("EMAIL_USER", "")
        self.password = os.getenv("EMAIL_PASSWORD", "")
    
    def send_email(self, to_email: str, subject: str, body: str, is_html: bool = False) -> bool:
        """Send email to recipient"""
        # Skip email if no credentials configured
        if not self.email or not self.password:
            print("Email service not configured - skipping email")
            return True  # Return True to not break the flow
            
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html' if is_html else 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            text = msg.as_string()
            server.sendmail(self.email, to_email, text)
            server.quit()
            
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
    
    def send_order_confirmation(self, to_email: str, order_id: str, total_amount: float) -> bool:
        """Send order confirmation email"""
        subject = f"Order Confirmation - {order_id}"
        body = f"""
        <html>
        <body>
            <h2>Thank you for your order!</h2>
            <p>Your order <strong>{order_id}</strong> has been confirmed.</p>
            <p>Total Amount: <strong>Kshs. {total_amount:,.2f}</strong></p>
            <p>We'll send you another email when your order ships.</p>
            <br>
            <p>Best regards,<br>Bloom Beauty Team</p>
        </body>
        </html>
        """
        return self.send_email(to_email, subject, body, is_html=True)
    
    def send_order_status_update(self, to_email: str, order_id: str, status: str) -> bool:
        """Send order status update email"""
        subject = f"Order Update - {order_id}"
        body = f"""
        <html>
        <body>
            <h2>Order Status Update</h2>
            <p>Your order <strong>{order_id}</strong> status has been updated to: <strong>{status}</strong></p>
            <br>
            <p>Best regards,<br>Bloom Beauty Team</p>
        </body>
        </html>
        """
        return self.send_email(to_email, subject, body, is_html=True)

# Create singleton instance
email_service = EmailService()