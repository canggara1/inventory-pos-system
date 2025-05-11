from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # e.g., Admin, Branch Head, Staff, Finance
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=True)

class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    location = db.Column(db.String(150))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    photo_url = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=0)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=False)
    production_date = db.Column(db.Date)
    expiration_date = db.Column(db.Date)

    def to_dict(self):
        return {
            'id': self.id,
            'item_id': self.item_id,
            'name': self.name,
            'photo_url': self.photo_url,
            'price': self.price,
            'quantity': self.quantity,
            'branch_id': self.branch_id,
            'production_date': self.production_date.strftime('%Y-%m-%d') if self.production_date else None,
            'expiration_date': self.expiration_date.strftime('%Y-%m-%d') if self.expiration_date else None
        }

class Transfer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=False)
    destination_branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    expiration_date = db.Column(db.Date)
    status = db.Column(db.String(20), nullable=False)  # Pending, In Transit, Completed, Cancelled
    notes = db.Column(db.Text)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    payment_type = db.Column(db.String(20), nullable=False)  # Cash, QRIS
    total = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime)
