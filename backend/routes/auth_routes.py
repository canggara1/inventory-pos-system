from flask import Blueprint, request, jsonify
from models import db, User
from utils import hash_password, verify_password, generate_token, token_required

bp = Blueprint('auth', __name__)

@bp.route('/protected', methods=['GET'])
@token_required
def protected_route(current_user):
    return jsonify({'message': 'This is a protected route', 'user': current_user.username})

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

@bp.route('/users', methods=['GET'])
@token_required
def list_users(current_user):
    users = User.query.all()
    users_data = [{
        'id': u.id,
        'username': u.username,
        'email': u.email,
        'user_type': u.user_type,
        'branch_id': u.branch_id
    } for u in users]
    return jsonify({'status': 'success', 'users': users_data})

@bp.route('/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(current_user, user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = hash_password(data['password'])
    if 'user_type' in data:
        user.user_type = data['user_type']
    if 'branch_id' in data:
        user.branch_id = data['branch_id']
    if 'permissions' in data:
        import json
        user.permissions = data['permissions']

    db.session.commit()
    return jsonify({'status': 'success', 'message': 'User updated successfully'})

@bp.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'User deleted successfully'})

@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username_or_email = data.get('username_or_email')
        password = data.get('password')

        if not username_or_email or not password:
            return jsonify({'status': 'error', 'message': 'Missing username/email or password'}), 400

        user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()
        if not user or not verify_password(user.password, password):
            return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401

        # Generate JWT token
        token = generate_token(user.id)

        return jsonify({
            'status': 'success',
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'user_type': user.user_type,
                'branch_id': user.branch_id
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
