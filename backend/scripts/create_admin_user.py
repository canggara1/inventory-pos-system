import sys
from backend.app import create_app, db
from backend.models import User
from backend.utils import hash_password

def create_admin(username, email, password):
    app = create_app()
    with app.app_context():
        if User.query.filter((User.username == username) | (User.email == email)).first():
            print("Admin user already exists.")
            return
        admin_user = User(
            username=username,
            email=email,
            password=hash_password(password),
            user_type='Administrator',
            branch_id=None
        )
        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin user '{username}' created successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python create_admin_user.py <username> <email> <password>")
        sys.exit(1)
    create_admin(sys.argv[1], sys.argv[2], sys.argv[3])
