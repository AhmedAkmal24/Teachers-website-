"""Script to list all users in the database."""
from app import create_app, db
from models import User

def list_users():
    """List all users in the database."""
    app = create_app()
    with app.app_context():
        users = User.query.all()
        
        print('\nUsers in database:')
        print('=' * 80)
        print(f"{'ID':<5} {'Name':<30} {'Email':<30} {'Role':<15}")
        print('-' * 80)
        
        if users:
            for user in users:
                print(f"{user.id:<5} {user.name:<30} {user.email:<30} {user.role:<15}")
        else:
            print("No users found in the database.")
        
        print('=' * 80)

if __name__ == '__main__':
    list_users()