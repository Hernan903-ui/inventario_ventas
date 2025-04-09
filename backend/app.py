from flask import Flask
from backend.extensions import db, migrate
from backend.routes.auth import auth_bp
from backend.routes.products import products_bp
from backend.routes.suppliers import suppliers_bp
from backend.routes.sales import sales_bp
from backend.routes.reports import reports_bp

def create_app():
    app = Flask(__name__, template_folder='../frontend/views')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key'

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(suppliers_bp, url_prefix='/suppliers')
    app.register_blueprint(sales_bp, url_prefix='/sales')
    app.register_blueprint(reports_bp, url_prefix='/reports')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)