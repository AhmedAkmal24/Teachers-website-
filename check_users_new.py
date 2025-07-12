"""Script to check users in the database."""
from app import create_app, db
from models import User

def check_users():
    """Display all users in the database."""
    app = create_app()
    with app.app_context():
        users = User.query.all()
        
        print('\nUsers in database:')
        for user in users:
            print(f'ID: {user.id}, Name: {user.name}, Email: {user.email}, Role: {user.role}')

if __name__ == '__main__':
    check_users()
