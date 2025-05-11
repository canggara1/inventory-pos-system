from flask import Blueprint, request, jsonify
from backend.models import db, Product

bp = Blueprint('inventory', __name__)

@bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    result = []
    for product in products:
        result.append({
            'id': product.id,
            'item_id': product.item_id,
            'name': product.name,
            'photo_url': product.photo_url,
            'price': product.price,
            'branch_id': product.branch_id,
            'production_date': product.production_date.isoformat() if product.production_date else None,
            'expiration_date': product.expiration_date.isoformat() if product.expiration_date else None
        })
    return jsonify(result)

@bp.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    product = Product(
        item_id=data.get('item_id'),
        name=data.get('name'),
        photo_url=data.get('photo_url'),
        price=data.get('price'),
        branch_id=data.get('branch_id'),
        production_date=data.get('production_date'),
        expiration_date=data.get('expiration_date')
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Product added successfully'})

@bp.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    product.item_id = data.get('item_id', product.item_id)
    product.name = data.get('name', product.name)
    product.photo_url = data.get('photo_url', product.photo_url)
    product.price = data.get('price', product.price)
    product.branch_id = data.get('branch_id', product.branch_id)
    product.production_date = data.get('production_date', product.production_date)
    product.expiration_date = data.get('expiration_date', product.expiration_date)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Product updated successfully'})

@bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Product deleted successfully'})
