from flask import Blueprint, request, jsonify
from models import db, Transfer, Product
from utils import token_required
from datetime import datetime

bp = Blueprint('transfers', __name__)

@bp.route('/', methods=['GET'])
@token_required
def get_transfers(current_user):
    try:
        branch_id_param = request.args.get('branch_id', type=int)
        if current_user.user_type == 'Administrator':
            query = Transfer.query
            if branch_id_param:
                query = query.filter((Transfer.source_branch_id == branch_id_param) | 
                                     (Transfer.destination_branch_id == branch_id_param))
        else:
            # Restrict to transfers involving user's branch only
            query = Transfer.query.filter(
                (Transfer.source_branch_id == current_user.branch_id) | 
                (Transfer.destination_branch_id == current_user.branch_id)
            )
        transfers = query.all()
        return jsonify([{
            'id': t.id,
            'source_branch_id': t.source_branch_id,
            'destination_branch_id': t.destination_branch_id,
            'product_id': t.product_id,
            'quantity': t.quantity,
            'expiration_date': t.expiration_date.strftime('%Y-%m-%d') if t.expiration_date else None,
            'status': t.status,
            'notes': t.notes
        } for t in transfers])
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/', methods=['POST'])
@token_required
def create_transfer(current_user):
    try:
        data = request.get_json()
        
        # Validate source product quantity
        source_product = Product.query.filter_by(
            id=data['product_id'],
            branch_id=data['source_branch_id']
        ).first()
        
        if not source_product:
            return jsonify({'status': 'error', 'message': 'Product not found in source branch'}), 404
        
        if source_product.quantity < data['quantity']:
            return jsonify({'status': 'error', 'message': 'Insufficient quantity in source branch'}), 400
        
        # Create transfer record
        transfer = Transfer(
            source_branch_id=data['source_branch_id'],
            destination_branch_id=data['destination_branch_id'],
            product_id=data['product_id'],
            quantity=data['quantity'],
            expiration_date=datetime.strptime(data['expiration_date'], '%Y-%m-%d') if data.get('expiration_date') else None,
            status='Pending',
            notes=data.get('notes')
        )
        
        # Reduce quantity from source branch
        source_product.quantity -= data['quantity']
        
        db.session.add(transfer)
        db.session.commit()
        
        return jsonify({'status': 'success', 'message': 'Transfer created successfully'})
    except KeyError as e:
        return jsonify({'status': 'error', 'message': f'Missing required field: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_transfer_status(current_user, id):
    try:
        transfer = Transfer.query.get_or_404(id)
        data = request.get_json()
        new_status = data.get('status')
        
        if not new_status:
            return jsonify({'status': 'error', 'message': 'Status is required'}), 400
        
        if new_status not in ['Pending', 'In Transit', 'Completed', 'Cancelled']:
            return jsonify({'status': 'error', 'message': 'Invalid status'}), 400
        
        old_status = transfer.status
        transfer.status = new_status
        
        # Handle inventory updates based on status change
        if new_status == 'Completed' and old_status != 'Completed':
            # Add quantity to destination branch
            dest_product = Product.query.filter_by(
                id=transfer.product_id,
                branch_id=transfer.destination_branch_id
            ).first()
            
            if not dest_product:
                # Create new product entry in destination branch
                source_product = Product.query.get(transfer.product_id)
                dest_product = Product(
                    item_id=source_product.item_id,
                    name=source_product.name,
                    photo_url=source_product.photo_url,
                    price=source_product.price,
                    quantity=0,
                    branch_id=transfer.destination_branch_id,
                    production_date=source_product.production_date,
                    expiration_date=source_product.expiration_date
                )
                db.session.add(dest_product)
            
            dest_product.quantity += transfer.quantity
            
        elif new_status == 'Cancelled' and old_status != 'Cancelled':
            # Return quantity to source branch
            source_product = Product.query.filter_by(
                id=transfer.product_id,
                branch_id=transfer.source_branch_id
            ).first()
            if source_product:
                source_product.quantity += transfer.quantity
        
        transfer.notes = data.get('notes', transfer.notes)
        db.session.commit()
        
        return jsonify({'status': 'success', 'message': 'Transfer status updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
