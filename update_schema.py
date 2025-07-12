"""Script to update the database schema."""
from app import create_app, db
from sqlalchemy import text

def update_database():
    """Add role column to user table."""
    app = create_app()
    with app.app_context():
        try:
            # Add role column to user table
            db.session.execute(text('ALTER TABLE user ADD COLUMN role VARCHAR(20) DEFAULT "student" NOT NULL'))
            db.session.commit()
            print('Database updated with role field')
        except Exception as e:
            print(f'Error updating database: {str(e)}')
            db.session.rollback()

if __name__ == '__main__':
    update_database()
