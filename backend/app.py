from flask import Flask
from .config import Config
from .extensions import db, migrate
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)  # Habilitar CORS
    app.config.from_object(Config)
    
    # Inicializar extensiones primero
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Registrar blueprints dentro del contexto de la aplicación
    with app.app_context():
        from . import models  # Importar modelos
        
        # Importar y registrar blueprints
        from .routes.auth import auth_bp
        from .routes.products import products_bp
        from .routes.reports import reports_bp
        from .routes.suppliers import suppliers_bp
        from .routes.analytics import analytics_bp

        app.register_blueprint(auth_bp, url_prefix='/api')
        app.register_blueprint(products_bp, url_prefix='/api')
        app.register_blueprint(reports_bp, url_prefix='/api')
        app.register_blueprint(suppliers_bp, url_prefix='/api')
        app.register_blueprint(analytics_bp, url_prefix='/api')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)