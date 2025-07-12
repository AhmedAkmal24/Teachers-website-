"""Lessons blueprint for teacher website."""
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from functools import wraps

from app import db
from models import Lesson

# Create a form for creating and editing lessons
class LessonForm(FlaskForm):
    title = StringField('Lesson Title', validators=[DataRequired(), Length(min=3, max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    content = TextAreaField('Lesson Content', validators=[DataRequired()])
    submit = SubmitField('Save Lesson')

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
bp = Blueprint('lessons', __name__, url_prefix='/lessons')

@bp.route('/')
@login_required
def index():
    """Show lessons based on user role."""
    if current_user.role == 'teacher':
        # Teachers see their own lessons
        lessons = Lesson.query.filter_by(teacher_id=current_user.id).order_by(Lesson.created.desc()).all()
    else:
        # Students see all lessons
        lessons = Lesson.query.order_by(Lesson.created.desc()).all()
    
    return render_template('lessons/index.html', lessons=lessons, is_teacher=(current_user.role == 'teacher'))

@bp.route('/create', methods=('GET', 'POST'))
@login_required
@teacher_required
def create():
    """Create a new lesson. Only teachers can access this route."""
    form = LessonForm()
    
    if form.validate_on_submit():
        lesson = Lesson(
            title=form.title.data,
            description=form.description.data,
            content=form.content.data,
            teacher_id=current_user.id
        )
        
        db.session.add(lesson)
        db.session.commit()
        
        flash('Lesson created successfully!', 'success')
        return redirect(url_for('lessons.index'))
        
    return render_template('lessons/create.html', form=form)

@bp.route('/<int:id>')
@login_required
def view(id):
    """View a specific lesson."""
    lesson = Lesson.query.get_or_404(id)
    
    # For teachers, enforce permission check - can only see their own lessons
    if current_user.role == 'teacher' and lesson.teacher_id != current_user.id:
        flash('You do not have permission to view this lesson.', 'danger')
        return redirect(url_for('lessons.index'))
        
    return render_template('lessons/view.html', lesson=lesson, is_teacher=(current_user.role == 'teacher'))

@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
@teacher_required
def edit(id):
    """Edit an existing lesson. Only teachers can access this route."""
    lesson = Lesson.query.get_or_404(id)
    
    # Make sure teacher can only edit their own lessons
    if lesson.teacher_id != current_user.id:
        flash('You do not have permission to edit this lesson.', 'danger')
        return redirect(url_for('lessons.index'))
    
    form = LessonForm()
    
    if request.method == 'GET':
        form.title.data = lesson.title
        form.description.data = lesson.description
        form.content.data = lesson.content
    
    if form.validate_on_submit():
        lesson.title = form.title.data
        lesson.description = form.description.data
        lesson.content = form.content.data
        
        db.session.commit()
        
        flash('Lesson updated successfully!', 'success')
        return redirect(url_for('lessons.view', id=lesson.id))
        
    return render_template('lessons/edit.html', form=form, lesson=lesson)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
@teacher_required
def delete(id):
    """Delete a lesson. Only teachers can access this route."""
    lesson = Lesson.query.get_or_404(id)
    
    # Make sure teacher can only delete their own lessons
    if lesson.teacher_id != current_user.id:
        flash('You do not have permission to delete this lesson.', 'danger')
        return redirect(url_for('lessons.index'))
    
    db.session.delete(lesson)
    db.session.commit()
    
    flash('Lesson deleted successfully!', 'success')
    return redirect(url_for('lessons.index'))
