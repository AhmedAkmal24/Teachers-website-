# Teacher Portal

A web application for teachers to manage lessons and school announcements, built with Flask.

## Features

- **User Authentication**: Secure registration and login for teachers
- **Dashboard**: View recent announcements and lessons
- **Lesson Management**: Create, edit, view, and delete lessons
- **Announcements**: Create, edit, view, and delete school-wide announcements
- **Profile**: View teacher profile information

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLAlchemy with SQLite
- **Frontend**: Bootstrap 5, HTML, CSS
- **Authentication**: Flask-Login

## Installation

1. Clone the repository:
```
git clone <repository-url>
cd teachers
```

2. Set up a virtual environment:
```
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Run the application:
```
python run.py
```

5. Access the application in your browser at `http://127.0.0.1:5000`

## Project Structure

- `/static` - CSS and static assets
- `/templates` - HTML templates
- `/instance` - Database file (created automatically)
- `models.py` - Database models
- `auth.py` - Authentication routes
- `dashboard.py` - Dashboard routes
- `lessons.py` - Lesson management routes
- `announcements.py` - Announcement management routes

## Usage

1. Register a new teacher account
2. Log in with your credentials
3. Use the dashboard to navigate to lessons and announcements
4. Create, edit, and manage your lessons
5. Create and view school announcements

## License

This project is licensed under the MIT License - see the LICENSE file for details.
