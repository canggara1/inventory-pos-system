from flask import Blueprint, request, jsonify
from backend.models import db, User
from backend.utils import hash_password, verify_password

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    user_type = data.get('user_type', 'Staff')
    branch_id = data.get('branch_id')

    if not username or not email or not password:
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'status': 'error', 'message': 'User already exists'}), 400

    new_user = User(
        username=username,
        email=email,
        password=hash_password(password),
        user_type=user_type,
        branch_id=branch_id
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'status': 'success', 'message': 'User registered successfully'})

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username_or_email = data.get('username_or_email')
    password = data.get('password')

    if not username_or_email or not password:
        return jsonify({'status': 'error', 'message': 'Missing username/email or password'}), 400

    user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()
    if not user or not verify_password(user.password, password):
        return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401

    # For simplicity, return user info (token-based auth can be added later)
    return jsonify({
        'status': 'success',
        'message': 'Login successful',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'user_type': user.user_type,
            'branch_id': user.branch_id
        }
    })
