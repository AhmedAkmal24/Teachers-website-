"""Script to add a new user to the database."""
from app import create_app, db
from models import User
from werkzeug.security import generate_password_hash
from datetime import datetime

def add_user(name, email, password, role='student'):
    """Add a new user to the database."""
    app = create_app()
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f"\nUser with email {email} already exists!")
            return
        
        # Create new user
        user = User(
            name=name,
            email=email,
            password=generate_password_hash(password),
            role=role,
            gender='other',  # Default value
            language_preference='en',
            theme_preference='light',
            created=datetime.utcnow()
        )
        
        # Add to database
        db.session.add(user)
        db.session.commit()
        
        print(f"\nNew user created successfully:")
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Role: {role}")
        print(f"Password: {password}")
        print("\nYou can now login with these credentials.")

if __name__ == '__main__':
    print("\nAdd a new user to the database")
    print("==============================")
    
    name = input("Enter name: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    role = input("Enter role (teacher or student) [default: student]: ") or "student"
    
    if role not in ['teacher', 'student']:
        print("Invalid role. Using 'student' as default.")
        role = 'student'
    
    add_user(name, email, password, role)
