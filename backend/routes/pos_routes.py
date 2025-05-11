from flask import Blueprint, request, jsonify
from backend.models import db, Transaction

bp = Blueprint('pos', __name__)

@bp.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    result = []
    for t in transactions:
        result.append({
            'id': t.id,
            'product_id': t.product_id,
            'quantity': t.quantity,
            'payment_type': t.payment_type,
            'total': t.total,
            'timestamp': t.timestamp.isoformat() if t.timestamp else None
        })
    return jsonify(result)

@bp.route('/transactions', methods=['POST'])
def create_transaction():
    data = request.get_json()
    transaction = Transaction(
        product_id=data.get('product_id'),
        quantity=data.get('quantity'),
        payment_type=data.get('payment_type'),
        total=data.get('total'),
        timestamp=data.get('timestamp')
    )
    db.session.add(transaction)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Transaction created successfully'})
