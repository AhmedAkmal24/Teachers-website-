# OTP (One Time Password) Feature - Configuration Guide

## What's been implemented:

1. **Database Changes**:
   - Added `otp_code`, `otp_expires`, and `otp_verified` columns to User model
   - Added `subject` field for teachers

2. **New Routes**:
   - `/auth/forgot-password` - Request OTP via email
   - `/auth/verify-otp` - Verify the OTP code
   - `/auth/reset-password` - Set new password after OTP verification

3. **Email Functionality**:
   - OTP generation (6-digit codes)
   - Email sending with HTML templates
   - OTP expiration (10 minutes)

4. **Templates Created**:
   - `forgot_password.html` - Request password reset
   - `verify_otp.html` - Enter OTP code
   - `reset_password.html` - Set new password

## To Enable Email Sending:

1. **Create a `.env` file** in the project root with your email settings:
```
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
```

2. **For Gmail users**:
   - Enable 2-Factor Authentication
   - Generate an App Password (not your regular password)
   - Use the 16-character app password in the .env file

3. **For other email providers**:
   - Update the SMTP settings in `email_utils.py`:
     - `smtp_server` (e.g., "smtp.outlook.com" for Outlook)
     - `smtp_port` (usually 587 for TLS)

## How to Test:

1. **Without Email** (for testing):
   - The OTP will be generated and stored in the database
   - You can check the database or modify the code to print the OTP
   - Comment out the email sending part in `forgot_password` route

2. **With Email**:
   - Set up your .env file
   - Click "Forgot Password?" on login page
   - Enter your email
   - Check your email for the OTP
   - Enter the OTP and set a new password

## Security Features:

- OTP expires after 10 minutes
- OTP is cleared after successful password reset
- Email existence is not revealed to prevent user enumeration
- Secure password requirements (minimum 8 characters)

## Demo Users:

- Email: `teacher@example.com`
- Password: `password123`
- Subject: `Mathematics` (for teachers)

You can now test the forgot password flow by:
1. Going to http://127.0.0.1:5000
2. Clicking "Forgot Password?"
3. Entering the email: teacher@example.com

The application is ready to use!
