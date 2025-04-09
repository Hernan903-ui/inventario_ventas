from flask import Flask, render_template

# Importar las extensiones
from backend.extensions import db, migrate

# Imports de blueprints
from backend.routes.products import products_bp
from backend.routes.sales import sales_bp
from backend.routes.analysis import analysis_bp
from backend.routes.suppliers import suppliers_bp
from backend.routes.reports import reports_bp

def create_app():
    app = Flask(__name__, template_folder='../frontend/views')

    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar las extensiones con la aplicación
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar blueprints
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(sales_bp, url_prefix='/sales')
    app.register_blueprint(analysis_bp, url_prefix='/analysis')
    app.register_blueprint(suppliers_bp, url_prefix='/suppliers')
    app.register_blueprint(reports_bp, url_prefix='/reports')

    # Rutas principales
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/sales')
    def sales():
        return render_template('sales.html')

    @app.route('/reports')
    def reports():
        return render_template('reports.html')
    
    @app.route('/products')
    def products():
        return render_template('products.html')
    
    @app.route('/suppliers')
    def suppliers():
        return render_template('suppliers.html')
    
    @app.route('/analysis')
    def analysis():
        return render_template('analysis.html')

    # Manejo de errores
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)