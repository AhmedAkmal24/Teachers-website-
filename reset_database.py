"""Script to reset the database."""
import os
import sys
from app import create_app, db
from models import User, Announcement, Lesson

def reset_database():
    """Drop all tables and recreate them with proper schemas."""
    app = create_app()
    with app.app_context():
        # Get the database file path
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        print(f"Database URI: {db_uri}")
        
        if db_uri.startswith('sqlite:///'):
            db_path = db_uri.replace('sqlite:///', '')
            print(f"Database file path: {db_path}")
            
            # Make sure the directory exists
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            
            # Delete the database file if it exists
            if os.path.exists(db_path):
                try:
                    # Close all connections
                    db.session.close()
                    # Remove the file
                    os.remove(db_path)
                    print(f"Database file {db_path} deleted")
                except Exception as e:
                    print(f"Error deleting database: {str(e)}")
                    
        # Drop all tables
        print("Dropping all tables...")
        db.drop_all()
        
        # Create all tables
        print("Creating all tables...")
        db.create_all()
        print("Database tables created successfully")
        
        # Print schema information
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        for table_name in inspector.get_table_names():
            print(f"\nTable: {table_name}")
            for column in inspector.get_columns(table_name):
                print(f"  {column['name']}: {column['type']}")

if __name__ == '__main__':
    reset_database()
