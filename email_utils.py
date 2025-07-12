"""Email utility functions for sending OTP and other emails."""
import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from flask import current_app
import os

def generate_otp():
    """Generate a 6-digit OTP."""
    return ''.join(random.choices(string.digits, k=6))

def send_otp_email(email, otp_code, name):
    """Send OTP code via email."""
    # Development mode - if no email config, just log the OTP
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    
    if not sender_email or not sender_password or sender_email == 'your_email@gmail.com':
        print("=" * 50)
        print("DEVELOPMENT MODE - Email not configured")
        print(f"OTP for {name} ({email}): {otp_code}")
        print("This OTP is valid for 10 minutes")
        print("=" * 50)
        return True, "OTP generated (check console/logs for code)"
    
    try:
        # Email configuration - you can modify these settings
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = "Password Reset OTP - Teacher Portal"
        message["From"] = sender_email
        message["To"] = email
        
        # Create HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #007bff; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .otp-code {{ font-size: 24px; font-weight: bold; color: #007bff; background-color: #f8f9fa; padding: 10px; text-align: center; margin: 20px 0; border-radius: 5px; }}
                .footer {{ background-color: #f8f9fa; padding: 15px; text-align: center; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Teacher Portal - Password Reset</h1>
                </div>
                <div class="content">
                    <h2>Hello {name},</h2>
                    <p>You have requested to reset your password. Please use the following One-Time Password (OTP) to complete the process:</p>
                    <div class="otp-code">{otp_code}</div>
                    <p><strong>Important:</strong></p>
                    <ul>
                        <li>This OTP is valid for 10 minutes only</li>
                        <li>Do not share this code with anyone</li>
                        <li>If you didn't request this, please ignore this email</li>
                    </ul>
                </div>
                <div class="footer">
                    <p>Teacher Portal © 2025 - Secure Password Reset</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Create plain text version
        text_content = f"""
        Teacher Portal - Password Reset
        
        Hello {name},
        
        You have requested to reset your password. Please use the following One-Time Password (OTP):
        
        OTP: {otp_code}
        
        Important:
        - This OTP is valid for 10 minutes only
        - Do not share this code with anyone
        - If you didn't request this, please ignore this email
        
        Teacher Portal © 2025
        """
        
        # Add parts to message
        part1 = MIMEText(text_content, "plain")
        part2 = MIMEText(html_content, "html")
        message.attach(part1)
        message.attach(part2)
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, message.as_string())
        
        return True, "OTP sent successfully"
        
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"

def is_otp_valid(user):
    """Check if user's OTP is still valid (not expired)."""
    if not user.otp_code or not user.otp_expires:
        return False
    
    return datetime.utcnow() < user.otp_expires

def clear_otp(user):
    """Clear OTP data from user."""
    user.otp_code = None
    user.otp_expires = None
    user.otp_verified = False
