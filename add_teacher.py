"""Script to add a teacher account to the database."""
from app import create_app, db
from models import User
from werkzeug.security import generate_password_hash
from datetime import datetime

def add_teacher(name, email, password, subject="Mathematics"):
    """Add a new teacher to the database."""
    try:
        print("Creating app context...")
        app = create_app()
        with app.app_context():
            # Check if user already exists
            print(f"Checking if email {email} already exists...")
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                print(f"\nUser with email {email} already exists! Cannot create duplicate account.")
                return
            
            print("Creating new teacher object...")
            # Create new teacher
            teacher = User(
                name=name,
                email=email,
                password=generate_password_hash(password),
                role='teacher',
                gender='other',  # Default value
                subject=subject,  # Teacher subject
                language_preference='en',
                theme_preference='light',
                created=datetime.utcnow()
            )
            
            # Add to database
            print("Adding to database session...")
            db.session.add(teacher)
            print("Committing to database...")
            db.session.commit()
            
            print(f"\nTeacher account created successfully:")
            print(f"Name: {name}")
            print(f"Email: {email}")
            print(f"Subject: {subject}")
            print(f"Password: {password}")
            print("\nYou can now login with these credentials.")
    except Exception as e:
        print(f"Error creating teacher account: {str(e)}")

# Add teacher account with default credentials
if __name__ == '__main__':
    # You can change these default values
    teacher_name = "Teacher Admin"
    teacher_email = "teacher@example.com"
    teacher_password = "password123"
    teacher_subject = "Mathematics"
    
    print(f"Starting script to add teacher: {teacher_email}")
    add_teacher(teacher_name, teacher_email, teacher_password, teacher_subject)
    print("Script completed.")
