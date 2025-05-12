import sys
import os
from werkzeug.security import generate_password_hash

# Adjust sys.path to import backend modules correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from app import create_app, db
from models import User

def create_admin(username, email, password):
    app = create_app()
    with app.app_context():
        admin_user = User(
            username=username,
            email=email,
            user_type='Administrator',
            branch_id=None,
            password=generate_password_hash(password)
        )
        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin user '{username}' created successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python create_admin_user.py <username> <email> <password>")
        sys.exit(1)
    username = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    create_admin(username, email, password)
