"""Announcements blueprint for teacher website."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from functools import wraps

from app import db
from models import Announcement

# Create a form for creating and editing announcements
class AnnouncementForm(FlaskForm):
    title = StringField('Announcement Title', validators=[DataRequired(), Length(min=3, max=100)])
    content = TextAreaField('Announcement Content', validators=[DataRequired()])
    submit = SubmitField('Save Announcement')

# Create a decorator to check if user is a teacher
def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'teacher':
            flash('Access denied. Teacher privileges required.', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

# Create blueprint
bp = Blueprint('announcements', __name__, url_prefix='/announcements')

@bp.route('/')
@login_required
def index():
    """Show all announcements."""
    announcements = Announcement.query.order_by(Announcement.created.desc()).all()
    return render_template('announcements/index.html', 
                          announcements=announcements, 
                          is_teacher=(current_user.role == 'teacher'))

@bp.route('/create', methods=('GET', 'POST'))
@login_required
@teacher_required
def create():
    """Create a new announcement. Only teachers can access this route."""
    form = AnnouncementForm()
    
    if form.validate_on_submit():
        announcement = Announcement(
            title=form.title.data,
            content=form.content.data,
            user_id=current_user.id
        )
        
        db.session.add(announcement)
        db.session.commit()
        
        flash('Announcement created successfully!', 'success')
        return redirect(url_for('announcements.index'))
        
    return render_template('announcements/create.html', form=form)

@bp.route('/<int:id>')
@login_required
def view(id):
    """View a specific announcement."""
    announcement = Announcement.query.get_or_404(id)
    return render_template('announcements/view.html', 
                          announcement=announcement, 
                          is_teacher=(current_user.role == 'teacher'))

@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
@teacher_required
def edit(id):
    """Edit an existing announcement. Only teachers can access this route."""
    announcement = Announcement.query.get_or_404(id)
    
    # Make sure teacher can only edit their own announcements
    if announcement.user_id != current_user.id:
        flash('You do not have permission to edit this announcement.', 'danger')
        return redirect(url_for('announcements.index'))
    
    form = AnnouncementForm()
    
    if request.method == 'GET':
        form.title.data = announcement.title
        form.content.data = announcement.content
    
    if form.validate_on_submit():
        announcement.title = form.title.data
        announcement.content = form.content.data
        
        db.session.commit()
        
        flash('Announcement updated successfully!', 'success')
        return redirect(url_for('announcements.view', id=announcement.id))
        
    return render_template('announcements/edit.html', form=form, announcement=announcement)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
@teacher_required
def delete(id):
    """Delete an announcement. Only teachers can access this route."""
    announcement = Announcement.query.get_or_404(id)
    
    # Make sure teacher can only delete their own announcements
    if announcement.user_id != current_user.id:
        flash('You do not have permission to delete this announcement.', 'danger')
        return redirect(url_for('announcements.index'))
    
    db.session.delete(announcement)
    db.session.commit()
    
    flash('Announcement deleted successfully!', 'success')
    return redirect(url_for('announcements.index'))
