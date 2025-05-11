from flask import Blueprint, request, jsonify
from backend.models import db, Transaction, Product, Transfer
from backend.utils import token_required
from datetime import datetime, timedelta
from sqlalchemy import func

bp = Blueprint('reports', __name__)

@bp.route('/daily', methods=['GET'])
@token_required
def daily_report(current_user):
    try:
        # Get date range from query parameters or default to today
        date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        date = datetime.strptime(date_str, '%Y-%m-%d')
        start_date = date.replace(hour=0, minute=0, second=0)
        end_date = date.replace(hour=23, minute=59, second=59)

        # Get daily sales
        daily_sales = db.session.query(
            func.sum(Transaction.total).label('total_sales'),
            func.count(Transaction.id).label('total_transactions')
        ).filter(
            Transaction.timestamp.between(start_date, end_date)
        ).first()

        # Get product stats
        product_stats = db.session.query(
            Product.id,
            Product.name,
            func.count(Transaction.id).label('sales_count'),
            func.sum(Transaction.total).label('sales_amount')
        ).join(
            Transaction
        ).filter(
            Transaction.timestamp.between(start_date, end_date)
        ).group_by(
            Product.id
        ).all()

        return jsonify({
            'status': 'success',
            'data': {
                'date': date_str,
                'sales': {
                    'total_amount': float(daily_sales.total_sales or 0),
                    'transaction_count': daily_sales.total_transactions or 0
                },
                'products': [{
                    'id': p.id,
                    'name': p.name,
                    'sales_count': p.sales_count,
                    'sales_amount': float(p.sales_amount or 0)
                } for p in product_stats]
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/inventory', methods=['GET'])
@token_required
def inventory_report(current_user):
    try:
        # Get products with low stock (less than 10 items)
        low_stock_products = Product.query.filter(
            Product.quantity < 10
        ).all()

        # Get products expiring within 30 days
        thirty_days = datetime.now() + timedelta(days=30)
        expiring_products = Product.query.filter(
            Product.expiration_date <= thirty_days
        ).all()

        # Get total inventory value
        inventory_value = db.session.query(
            func.sum(Product.price * Product.quantity).label('total_value')
        ).first()

        return jsonify({
            'status': 'success',
            'data': {
                'low_stock': [{
                    'id': p.id,
                    'name': p.name,
                    'quantity': p.quantity
                } for p in low_stock_products],
                'expiring_soon': [{
                    'id': p.id,
                    'name': p.name,
                    'expiration_date': p.expiration_date.strftime('%Y-%m-%d')
                } for p in expiring_products],
                'total_value': float(inventory_value.total_value or 0)
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
