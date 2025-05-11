from flask import Blueprint, request, jsonify
from models import db, Product
from utils import token_required
from datetime import datetime

bp = Blueprint('inventory', __name__)

@bp.route('/products', methods=['GET'])
@token_required
def get_products(current_user):
    try:
        branch_id = request.args.get('branch_id', type=int)
        query = Product.query
        if branch_id:
            query = query.filter_by(branch_id=branch_id)
        products = query.all()
        return jsonify([product.to_dict() for product in products])
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/products', methods=['POST'])
@token_required
def add_product(current_user):
    try:
        data = request.get_json()
        product = Product(
            item_id=data['item_id'],
            name=data['name'],
            photo_url=data.get('photo_url'),
            price=data['price'],
            quantity=data.get('quantity', 0),
            branch_id=data['branch_id'],
            production_date=datetime.strptime(data['production_date'], '%Y-%m-%d') if data.get('production_date') else None,
            expiration_date=datetime.strptime(data['expiration_date'], '%Y-%m-%d') if data.get('expiration_date') else None
        )
        db.session.add(product)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Product added successfully', 'product': product.to_dict()})
    except KeyError as e:
        return jsonify({'status': 'error', 'message': f'Missing required field: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/products/<int:id>', methods=['PUT'])
@token_required
def update_product(current_user, id):
    try:
        product = Product.query.get_or_404(id)
        data = request.get_json()
        
        if 'item_id' in data:
            product.item_id = data['item_id']
        if 'name' in data:
            product.name = data['name']
        if 'photo_url' in data:
            product.photo_url = data['photo_url']
        if 'price' in data:
            product.price = data['price']
        if 'quantity' in data:
            product.quantity = data['quantity']
        if 'branch_id' in data:
            product.branch_id = data['branch_id']
        if 'production_date' in data:
            product.production_date = datetime.strptime(data['production_date'], '%Y-%m-%d') if data['production_date'] else None
        if 'expiration_date' in data:
            product.expiration_date = datetime.strptime(data['expiration_date'], '%Y-%m-%d') if data['expiration_date'] else None

        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Product updated successfully', 'product': product.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/products/<int:id>', methods=['DELETE'])
@token_required
def delete_product(current_user, id):
    try:
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Product deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/products/adjust-quantity/<int:id>', methods=['POST'])
@token_required
def adjust_quantity(current_user, id):
    try:
        product = Product.query.get_or_404(id)
        data = request.get_json()
        
        if 'adjustment' not in data:
            return jsonify({'status': 'error', 'message': 'Adjustment value is required'}), 400
            
        product.quantity += data['adjustment']
        if product.quantity < 0:
            return jsonify({'status': 'error', 'message': 'Insufficient quantity'}), 400
            
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Quantity adjusted successfully', 'product': product.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
