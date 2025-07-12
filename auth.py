"""Authentication blueprint for teacher website."""
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional

from app import db, login_manager
from models import User

# Create a class for the login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

# Create a class for the registration form
class RegisterForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[Optional(), Length(min=5, max=20)])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], validators=[DataRequired()])
    grade = StringField('Grade/Class', validators=[Optional(), Length(max=20)])
    school = StringField('School', validators=[Optional(), Length(max=100)])
    subject = StringField('Subject', validators=[Optional(), Length(max=100)])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    role = RadioField('Register as', choices=[('student', 'Student'), ('teacher', 'Teacher')], 
                     default='student', validators=[DataRequired()])
    language = SelectField('Language', choices=[('en', 'English'), ('ar', 'العربية')], default='en')
    theme = SelectField('Theme', choices=[('light', 'Light'), ('dark', 'Dark')], default='light')
    submit = SubmitField('Register')

# Create a class for the forgot password form
class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send OTP')

# Create a class for the OTP verification form
class VerifyOTPForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    otp_code = StringField('OTP Code', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField('Verify OTP')

# Create a class for the reset password form
class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match')
    ])
    submit = SubmitField('Reset Password')

# Create blueprint
bp = Blueprint('auth', __name__, url_prefix='/auth')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            # Normalize email to lowercase and strip whitespace
            email = form.email.data.strip().lower()
            
            # Check if email already exists (case-insensitive)
            existing_user = User.query.filter(User.email.ilike(email)).first()
            if existing_user:
                flash('Email already registered. Please use a different email or log in.', 'danger')
                return render_template('auth/register.html', form=form)
            
            # Create new user with normalized email
            user = User(
                name=form.name.data,
                email=email,  # Use normalized email
                password=generate_password_hash(form.password.data),
                role=form.role.data,
                phone_number=form.phone_number.data,
                gender=form.gender.data,
                grade=form.grade.data,
                school=form.school.data,
                subject=form.subject.data,
                language_preference=form.language.data,
                theme_preference=form.theme.data
            )
            
            # Add to database
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f'Error during registration: {str(e)}', 'danger')
    
    return render_template('auth/register.html', form=form)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            email = form.email.data.strip().lower()
            print(f"Attempting login for email: {email}")
            
            # Debug - Check all users in database
            all_users = User.query.all()
            print(f"All users in database: {[user.email for user in all_users]}")
            
            # First try exact match
            user = User.query.filter_by(email=email).first()
            
            # If not found, try case-insensitive search
            if not user:
                print("Attempting case-insensitive search")
                user = User.query.filter(User.email.ilike(email)).first()
            
            if user:
                print(f"User found: {user.name}, Role: {user.role}, Email: {user.email}")
                if check_password_hash(user.password, form.password.data):
                    login_user(user)
                    next_page = request.args.get('next')
                    
                    # Store user preferences in session
                    session['language'] = user.language_preference
                    session['theme'] = user.theme_preference
                    
                    print(f"Login successful for {user.email}")
                    flash('Login successful!', 'success')
                    return redirect(next_page or url_for('dashboard.index'))
                else:
                    print("Password incorrect")
                    flash('Login unsuccessful. Incorrect password.', 'danger')
            else:
                print(f"No user found with email: {email}")
                flash('Login unsuccessful. Email not found.', 'danger')
        except Exception as e:
            print(f"Login error: {str(e)}")
            flash(f'Login error: {str(e)}', 'danger')
    
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    # Preserve language and theme preferences in session
    language = session.get('language', 'en')
    theme = session.get('theme', 'light')
    
    logout_user()
    
    # Restore language and theme preferences
    session['language'] = language
    session['theme'] = theme
    
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@bp.route('/forgot-password', methods=('GET', 'POST'))
def forgot_password():
    """Handle forgot password - send OTP to email."""
    form = ForgotPasswordForm()
    
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        user = User.query.filter(User.email.ilike(email)).first()
        
        if user:
            # Generate OTP
            from email_utils import generate_otp, send_otp_email
            from datetime import datetime, timedelta
            
            otp_code = generate_otp()
            user.otp_code = otp_code
            user.otp_expires = datetime.utcnow() + timedelta(minutes=10)  # OTP valid for 10 minutes
            user.otp_verified = False
            
            # Send OTP via email
            success, message = send_otp_email(user.email, otp_code, user.name)
            
            if success:
                db.session.commit()
                # Show different message based on whether email was actually sent
                if "check console" in message.lower():
                    flash(f'Development Mode: Your OTP is {otp_code}. This code is valid for 10 minutes.', 'info')
                else:
                    flash('OTP has been sent to your email. Please check your inbox.', 'success')
                return redirect(url_for('auth.verify_otp', email=email))
            else:
                flash('Failed to send OTP. Please try again later.', 'danger')
        else:
            # Don't reveal if email exists or not for security
            flash('If this email is registered, you will receive an OTP shortly.', 'info')
            
    return render_template('auth/forgot_password.html', form=form)

@bp.route('/verify-otp', methods=('GET', 'POST'))
def verify_otp():
    """Handle OTP verification."""
    form = VerifyOTPForm()
    email = request.args.get('email', '')
    
    if request.method == 'GET':
        form.email.data = email
    
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        otp_code = form.otp_code.data
        
        user = User.query.filter(User.email.ilike(email)).first()
        
        if user and user.otp_code == otp_code:
            from email_utils import is_otp_valid
            
            if is_otp_valid(user):
                user.otp_verified = True
                db.session.commit()
                flash('OTP verified successfully. You can now reset your password.', 'success')
                return redirect(url_for('auth.reset_password', email=email))
            else:
                flash('OTP has expired. Please request a new one.', 'danger')
                return redirect(url_for('auth.forgot_password'))
        else:
            flash('Invalid OTP. Please try again.', 'danger')
            
    return render_template('auth/verify_otp.html', form=form)

@bp.route('/reset-password', methods=('GET', 'POST'))
def reset_password():
    """Handle password reset after OTP verification."""
    form = ResetPasswordForm()
    email = request.args.get('email', '')
    
    if request.method == 'GET':
        form.email.data = email
    
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        user = User.query.filter(User.email.ilike(email)).first()
        
        if user and user.otp_verified:
            from email_utils import is_otp_valid, clear_otp
            
            if is_otp_valid(user):
                # Update password
                user.password = generate_password_hash(form.new_password.data)
                
                # Clear OTP data
                clear_otp(user)
                db.session.commit()
                
                flash('Password reset successfully! You can now login with your new password.', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('Session expired. Please start the password reset process again.', 'danger')
                return redirect(url_for('auth.forgot_password'))
        else:
            flash('Invalid request. Please verify your OTP first.', 'danger')
            return redirect(url_for('auth.forgot_password'))
            
    return render_template('auth/reset_password.html', form=form)
