"""Add OTP columns to existing database."""
from app import create_app, db
import sqlite3
import os

def add_otp_columns():
    """Add OTP columns to existing user table."""
    print("Adding OTP columns to database...")
    
    app = create_app()
    db_path = os.path.join(app.instance_path, 'teachers.sqlite')
    
    if not os.path.exists(db_path):
        print("Database doesn't exist. Creating new database...")
        with app.app_context():
            db.create_all()
            print("Database created with all new fields!")
        return
    
    try:
        # Connect directly to SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if OTP columns already exist
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        
        print(f"Current columns: {columns}")
        
        # Add OTP columns if they don't exist
        if 'otp_code' not in columns:
            cursor.execute("ALTER TABLE user ADD COLUMN otp_code VARCHAR(6)")
            print("Added otp_code column")
        
        if 'otp_expires' not in columns:
            cursor.execute("ALTER TABLE user ADD COLUMN otp_expires DATETIME")
            print("Added otp_expires column")
        
        if 'otp_verified' not in columns:
            cursor.execute("ALTER TABLE user ADD COLUMN otp_verified BOOLEAN DEFAULT 0")
            print("Added otp_verified column")
        
        # Add subject column if it doesn't exist
        if 'subject' not in columns:
            cursor.execute("ALTER TABLE user ADD COLUMN subject VARCHAR(100)")
            print("Added subject column")
        
        conn.commit()
        conn.close()
        
        print("Database migration completed successfully!")
        
    except Exception as e:
        print(f"Error during migration: {str(e)}")

if __name__ == '__main__':
    add_otp_columns()
