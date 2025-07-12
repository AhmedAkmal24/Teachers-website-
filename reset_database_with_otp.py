"""Reset and recreate the database with all new fields."""
from app import create_app, db
from models import User, Announcement, Lesson
import os

def reset_database():
    """Reset the database and recreate all tables."""
    print("Resetting database...")
    
    app = create_app()
    with app.app_context():
        # Get the database file path
        db_path = os.path.join(app.instance_path, 'teachers.sqlite')
        
        # Remove existing database if it exists
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"Removed existing database: {db_path}")
        
        # Create instance directory if it doesn't exist
        os.makedirs(app.instance_path, exist_ok=True)
        
        # Create all tables
        db.create_all()
        print("Created new database with all tables!")
        print("Database schema updated with:")
        print("- User table with subject and OTP fields")
        print("- Announcement table")
        print("- Lesson table")
        
        print("\nDatabase reset complete!")
        print("You can now run the application or add test users.")

if __name__ == '__main__':
    reset_database()
