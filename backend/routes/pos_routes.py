from flask import Blueprint, request, jsonify
from models import db, Transaction, Product
from utils import token_required
from datetime import datetime

bp = Blueprint('pos', __name__)

@bp.route('/transactions', methods=['GET'])
@token_required
def get_transactions(current_user):
    try:
        branch_id = request.args.get('branch_id', type=int)
        date_str = request.args.get('date')
        
        query = Transaction.query
        
        if branch_id:
            query = query.join(Product).filter(Product.branch_id == branch_id)
            
        if date_str:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            start_date = date.replace(hour=0, minute=0, second=0)
            end_date = date.replace(hour=23, minute=59, second=59)
            query = query.filter(Transaction.timestamp.between(start_date, end_date))
            
        transactions = query.all()
        return jsonify([{
            'id': t.id,
            'product_id': t.product_id,
            'quantity': t.quantity,
            'payment_type': t.payment_type,
            'total': t.total,
            'timestamp': t.timestamp.isoformat() if t.timestamp else None
        } for t in transactions])
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/transactions', methods=['POST'])
@token_required
def create_transaction(current_user):
    try:
        data = request.get_json()
        
        # Validate product and quantity
        product = Product.query.get_or_404(data['product_id'])
        
        if product.quantity < data['quantity']:
            return jsonify({
                'status': 'error',
                'message': 'Insufficient stock'
            }), 400
            
        # Calculate total
        total = product.price * data['quantity']
        
        # Create transaction
        transaction = Transaction(
            product_id=data['product_id'],
            quantity=data['quantity'],
            payment_type=data['payment_type'],
            total=total,
            timestamp=datetime.now()
        )
        
        # Update product quantity
        product.quantity -= data['quantity']
        
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Transaction created successfully',
            'transaction': {
                'id': transaction.id,
                'product_id': transaction.product_id,
                'quantity': transaction.quantity,
                'payment_type': transaction.payment_type,
                'total': transaction.total,
                'timestamp': transaction.timestamp.isoformat()
            }
        })
    except KeyError as e:
        return jsonify({'status': 'error', 'message': f'Missing required field: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/transactions/<int:id>', methods=['GET'])
@token_required
def get_transaction(current_user, id):
    try:
        transaction = Transaction.query.get_or_404(id)
        return jsonify({
            'id': transaction.id,
            'product_id': transaction.product_id,
            'quantity': transaction.quantity,
            'payment_type': transaction.payment_type,
            'total': transaction.total,
            'timestamp': transaction.timestamp.isoformat() if transaction.timestamp else None
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
