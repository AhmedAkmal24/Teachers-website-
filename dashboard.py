"""Dashboard blueprint for teacher website."""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from models import Announcement, Lesson, User

# Create blueprint
bp = Blueprint('dashboard', __name__)

@bp.route('/')
@login_required
def index():
    """Show dashboard with content based on user role (teacher or student)."""
    recent_announcements = Announcement.query.order_by(Announcement.created.desc()).limit(5).all()
    
    # Show lessons based on user role
    if current_user.role == 'teacher':
        # Teachers see lessons they created
        recent_lessons = Lesson.query.filter_by(teacher_id=current_user.id).order_by(Lesson.created.desc()).limit(5).all()
    else:  # Student
        # Students see all lessons
        recent_lessons = Lesson.query.order_by(Lesson.created.desc()).limit(5).all()
    
    return render_template('dashboard/index.html', 
                           announcements=recent_announcements,
                           lessons=recent_lessons,
                           is_teacher=(current_user.role == 'teacher'))

@bp.route('/profile')
@login_required
def profile():
    """Show teacher profile page."""
    return render_template('dashboard/profile.html')

@bp.route('/save-preference', methods=['POST'])
@login_required
def save_preference():
    """Save user preference (theme, language) to database."""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    key = data.get('key')
    value = data.get('value')
    
    if key not in ['theme', 'language']:
        return jsonify({"error": "Invalid preference key"}), 400
    
    # Update the appropriate field
    if key == 'theme':
        current_user.theme_preference = value
    elif key == 'language':
        current_user.language_preference = value
    
    # Save to database
    db.session.commit()
    
    return jsonify({"success": True}), 200

@bp.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    """Update user profile information."""
    # Get form data
    name = request.form.get('name')
    email = request.form.get('email')
    phone_number = request.form.get('phone_number')
    gender = request.form.get('gender')
    grade = request.form.get('grade') if current_user.role == 'student' else None
    school = request.form.get('school') if current_user.role == 'student' else None
    subject = request.form.get('subject') if current_user.role == 'teacher' else None
    language = request.form.get('language')
    theme = request.form.get('theme')
    
    # Check if email is already in use by another user
    existing_user = User.query.filter(User.email == email, User.id != current_user.id).first()
    if existing_user:
        flash('Email already in use by another account.', 'danger')
        return redirect(url_for('dashboard.profile'))
    
    # Update user information
    current_user.name = name
    current_user.email = email
    current_user.phone_number = phone_number
    current_user.gender = gender
    current_user.grade = grade
    current_user.school = school
    current_user.subject = subject
    current_user.language_preference = language
    current_user.theme_preference = theme
    
    # Save to database
    db.session.commit()
    
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('dashboard.profile'))
