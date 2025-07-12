"""Test the OTP email functionality in development mode."""
from email_utils import send_otp_email, generate_otp

def test_development_mode():
    """Test OTP email in development mode."""
    print("Testing OTP email functionality in development mode...")
    
    # Generate a test OTP
    otp = generate_otp()
    print(f"Generated OTP: {otp}")
    
    # Test sending email in development mode
    success, message = send_otp_email("test@example.com", otp, "Test User")
    
    print(f"Success: {success}")
    print(f"Message: {message}")
    
    if success:
        print("✅ OTP functionality is working in development mode!")
    else:
        print("❌ OTP functionality failed")

if __name__ == '__main__':
    test_development_mode()
