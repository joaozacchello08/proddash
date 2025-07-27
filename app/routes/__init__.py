from flask import Flask
from .user_routes import user_bp
from .dashboard_routes import dashboard_bp
from .product_routes import product_bp
from .sales_routes import sales_bp

def register_routes(app: Flask):
    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboards")
    app.register_blueprint(product_bp, url_prefix="/api/products")
    app.register_blueprint(sales_bp, url_prefix="/api/sales")
