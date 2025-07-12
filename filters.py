"""Custom Jinja filters for the teacher website."""
from flask import Flask

def nl2br(value):
    """Convert newlines to HTML line breaks."""
    if not value:
        return ""
    return value.replace('\n', '<br>')

def init_app(app):
    """Initialize custom Jinja filters."""
    app.jinja_env.filters['nl2br'] = nl2br
