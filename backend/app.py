from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    import sys
    sys.path.insert(0, '')
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    from routes.auth_routes import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    from routes.inventory_routes import bp as inventory_bp
    app.register_blueprint(inventory_bp, url_prefix='/api/inventory')

    from routes.transfer_routes import bp as transfer_bp
    app.register_blueprint(transfer_bp, url_prefix='/api/transfers')

    from routes.pos_routes import bp as pos_bp
    app.register_blueprint(pos_bp, url_prefix='/api/pos')

    from routes.report_routes import bp as report_bp
    app.register_blueprint(report_bp, url_prefix='/api/reports')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=5000)
