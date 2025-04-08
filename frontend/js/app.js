from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    with app.app_context():
        from .models import Business, User, Supplier, Product, ProductHistory
        db.create_all()
        
        # Registrar blueprints
        from .routes.auth import auth_bp
        from .routes.products import products_bp
        from .routes.analytics import analytics_bp
        from .routes.reports import reports_bp
        
        app.register_blueprint(auth_bp)
        app.register_blueprint(products_bp)
        app.register_blueprint(analytics_bp)
        app.register_blueprint(reports_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)