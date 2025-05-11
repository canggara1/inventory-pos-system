from flask import Blueprint, request, jsonify
from backend.models import db, Transfer

bp = Blueprint('transfers', __name__)

@bp.route('/', methods=['GET'])
def get_transfers():
    transfers = Transfer.query.all()
    result = []
    for t in transfers:
        result.append({
            'id': t.id,
            'source_branch_id': t.source_branch_id,
            'destination_branch_id': t.destination_branch_id,
            'product_id': t.product_id,
            'quantity': t.quantity,
            'expiration_date': t.expiration_date.isoformat() if t.expiration_date else None,
            'status': t.status,
            'notes': t.notes
        })
    return jsonify(result)

@bp.route('/', methods=['POST'])
def create_transfer():
    data = request.get_json()
    transfer = Transfer(
        source_branch_id=data.get('source_branch_id'),
        destination_branch_id=data.get('destination_branch_id'),
        product_id=data.get('product_id'),
        quantity=data.get('quantity'),
        expiration_date=data.get('expiration_date'),
        status='Pending',
        notes=data.get('notes')
    )
    db.session.add(transfer)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Transfer created successfully'})

@bp.route('/<int:id>', methods=['PUT'])
def update_transfer(id):
    transfer = Transfer.query.get_or_404(id)
    data = request.get_json()
    transfer.status = data.get('status', transfer.status)
    transfer.notes = data.get('notes', transfer.notes)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Transfer updated successfully'})
