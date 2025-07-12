"""Script to clear all data from the database."""
from app import create_app, db
from models import User, Announcement, Lesson

def clear_database():
    """Remove all data from the database but keep the structure."""
    app = create_app()
    with app.app_context():
        try:
            # Delete all records from tables
            print("Deleting all lessons...")
            Lesson.query.delete()
            
            print("Deleting all announcements...")
            Announcement.query.delete()
            
            print("Deleting all users...")
            User.query.delete()
            
            # Commit the changes
            db.session.commit()
            print("\nDatabase cleared successfully! All records have been removed.")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error clearing database: {str(e)}")

if __name__ == '__main__':
    print("=== Database Clearing Tool ===")
    confirm = input("Are you sure you want to clear all data from the database? This cannot be undone. (yes/no): ")
    
    if confirm.lower() == 'yes':
        clear_database()
    else:
        print("Operation cancelled. Database remains unchanged.")
