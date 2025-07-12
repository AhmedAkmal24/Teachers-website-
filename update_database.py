"""Update database with new user fields."""
from app import create_app, db
from models import User
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        # Create the tables if they don't exist
        db.create_all()
        print("Database tables updated!")
