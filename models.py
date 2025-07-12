"""Database models for teacher website."""
from datetime import datetime
from flask_login import UserMixin
from app import db

class User(db.Model, UserMixin):
    """User model for teachers and students."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')  # 'teacher' or 'student'
    phone_number = db.Column(db.String(20), nullable=True)
    gender = db.Column(db.String(10), nullable=True)  # 'male', 'female', or 'other'
    grade = db.Column(db.String(20), nullable=True)  # For students
    school = db.Column(db.String(100), nullable=True)
    subject = db.Column(db.String(100), nullable=True)  # For teachers
    language_preference = db.Column(db.String(10), default='en')  # 'en' or 'ar'
    theme_preference = db.Column(db.String(10), default='light')  # 'light' or 'dark'
    created = db.Column(db.DateTime, default=datetime.utcnow)
    
    # OTP fields for password reset
    otp_code = db.Column(db.String(6), nullable=True)  # 6-digit OTP
    otp_expires = db.Column(db.DateTime, nullable=True)  # OTP expiration time
    otp_verified = db.Column(db.Boolean, default=False)  # Whether OTP is verified
    
    # Relationships
    announcements = db.relationship('Announcement', backref='author', lazy=True)
    lessons = db.relationship('Lesson', backref='teacher', lazy=True)
    
    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"

class Announcement(db.Model):
    """Announcement model for school-wide announcements."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Announcement('{self.title}', '{self.created}')"

class Lesson(db.Model):
    """Lesson model for teacher lessons."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Lesson('{self.title}', '{self.created}')"
