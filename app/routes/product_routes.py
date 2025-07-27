from flask import Blueprint, request, abort, jsonify
from app.extensions import db
from app.models import Dashboard, Product


product_bp = Blueprint("product_bp", __name__)

#region products
#region CREATE product
@product_bp.route("/", methods=["POST"])
def create_product():
    body = request.json

    if not body:
        abort(400)

    dashboard_id = body.get("dashboardId")
    product_name = body.get("productName")
    product_price = body.get("productPrice")
    product_stock = body.get("productStock", 0)
    product_image = body.get("productImage")
    product_barcode = body.get("productBarcode")
    product_cost = body.get("productCost")

    if not all([dashboard_id, product_name, product_price is not None]):
        abort(400)

    try:
        dashboard = db.session.get(Dashboard, dashboard_id)
        if not dashboard:
            abort(404)
        
        if Product.query.filter_by(dashboardId=dashboard_id, productName=product_name).first() or Product.query.filter_by(dashboardId=dashboard_id, productBarcode=product_barcode).first():
            abort(409)
        
        new_product = Product(
            productName=product_name,
            productPrice=float(product_price),
            productStock=int(product_stock),
            productImage=product_image,
            productBarcode=product_barcode,
            productCost=float(product_cost) if product_cost is not None else None
        )

        new_product.dashboard = dashboard

        db.session.add(new_product)
        db.session.commit()
    except Exception as e:
        print(f"Error: {str(e)}")
        abort(500)
    
    return jsonify({ "message": "Product created successfully!", "newProduct": new_product.serialize() }), 201
#endregion

#region UPDATE product
@product_bp.route("/", methods=["UPDATE"])
def update_product():
    body = request.json

    if not body:
        abort(400)
    
    product_id = body.get("productId")
    updates = body.get("updates")

    if not all([product_id, updates]):
        abort(400)

    allowed_updates = ["productName", "productImage", "productPrice", "productCost", "productBarcode", "productStock"]

    try:
        product = db.session.get(Product, product_id)
        if not product:
            abort(404)

        for update in updates:
            for key, value in update.items():
                if key in allowed_updates:
                    setattr(product, key, value)
        
        db.session.commit()
    except Exception as e:
        print(f"Error: {str(e)}")
        abort(500)
    
    return jsonify({ "updatedProduct": product.serialize() }), 200
#endregion

#region DELETE product
@product_bp.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id: int):
    try:
        product = db.session.get(Product, product_id)
        if not product:
            abort(404)
        db.session.delete(product)
        db.session.commit()
    except Exception as e:
        print(f"Error: {str(e)}")
        abort(500)
    
    return jsonify({ "deletedProduct": product.serialzie(), "message": "Product deleted successfully!" }), 200
#endregion
#endregion

#region READ
@product_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id: int):
    product = db.session.get(Product, product_id)
    if not product:
        abort(404)
    return jsonify({ "product": product.serialize() }), 200

@product_bp.route("/by-dashboard/<int:dashboard_id>", methods=["GET"])
def get_dashboard_products(dashboard_id: int):
    dashboard = db.session.get(Dashboard, dashboard_id)
    if not dashboard:
        abort(404)
    return jsonify({ "products": [product.serialize() for product in dashboard.products] }), 200
#endregion
