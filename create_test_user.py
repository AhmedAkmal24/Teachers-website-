"""Script to create a test user."""
from app import create_app, db
from models import User
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_test_user():
    """Create a test user for login testing."""
    try:
        print("Starting test user creation...")
        app = create_app()
        with app.app_context():
            # List all users first
            print("Current users in database:")
            all_users = User.query.all()
            for user in all_users:
                print(f"- {user.email} (role: {user.role})")
                
            # Check if test user already exists
            test_user = User.query.filter_by(email='test@example.com').first()
            if test_user:
                print("Test user already exists.")
                return
                
            print("Creating new test user...")
            # Create test user
            test_user = User(
                name='Test User',
                email='test@example.com',
                password=generate_password_hash('testpassword'),
                role='student',
                phone_number='1234567890',
                gender='other',
                language_preference='en',
                theme_preference='light',
                created=datetime.utcnow()
            )
            
            # Add to database
            db.session.add(test_user)
            db.session.commit()
            
            print("Test user created:")
            print(f"Email: test@example.com")
            print(f"Password: testpassword")
    except Exception as e:
        print(f"Error creating test user: {str(e)}")

if __name__ == '__main__':
    create_test_user()
