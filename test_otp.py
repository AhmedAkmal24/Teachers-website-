"""Test script for OTP functionality without actually sending emails."""
from app import create_app, db
from models import User
from email_utils import generate_otp, is_otp_valid, clear_otp
from datetime import datetime, timedelta

def test_otp_functionality():
    """Test OTP generation and validation."""
    print("Testing OTP functionality...")
    
    app = create_app()
    with app.app_context():
        # Test OTP generation
        otp = generate_otp()
        print(f"Generated OTP: {otp}")
        
        # Test finding a user (you can modify this email to match a user in your database)
        test_email = "teacher@example.com"
        user = User.query.filter(User.email.ilike(test_email)).first()
        
        if user:
            print(f"Found user: {user.name} ({user.email})")
            
            # Set OTP for user
            user.otp_code = otp
            user.otp_expires = datetime.utcnow() + timedelta(minutes=10)
            user.otp_verified = False
            
            print(f"OTP set for user: {user.otp_code}")
            print(f"OTP expires at: {user.otp_expires}")
            
            # Test OTP validation
            if is_otp_valid(user):
                print("✓ OTP is valid")
            else:
                print("✗ OTP is invalid or expired")
            
            # Test OTP clearing
            clear_otp(user)
            print("OTP cleared from user")
            
            if user.otp_code is None:
                print("✓ OTP successfully cleared")
            else:
                print("✗ OTP not cleared properly")
                
        else:
            print(f"No user found with email: {test_email}")
            print("Create a user first using the add_teacher.py script or register through the web interface")

if __name__ == '__main__':
    test_otp_functionality()
