import sys
import os

# Adjust sys.path to import backend modules correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from models import User

def create_admin():
    app = create_app()
    with app.app_context():
        username = input("Enter admin username: ")
        email = input("Enter admin email: ")
        password = input("Enter admin password: ")

        admin_user = User(
            username=username,
            email=email,
            user_type='Administrator',
            branch_id=None
        )
        admin_user.set_password(password)
        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin user '{username}' created successfully.")

if __name__ == "__main__":
    create_admin()
