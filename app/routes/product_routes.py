from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import User, Dashboard, Product
from flask_jwt_extended import get_jwt_identity, jwt_required


product_bp = Blueprint("product_bp", __name__)

#region create product
@product_bp.route("/", methods=["POST"])
@jwt_required()
def create_product():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({ "message": "User not found" }), 404
    
    dashboard = user.dashboard
    if not dashboard:
        return jsonify({ "message": "Couldn't find this user dashboard" }), 404
    
    body = request.json
    if not body:
        return jsonify({ "message": "No JSON found on request" }), 400
    
    productName = body.get("productName")
    productImage = body.get("productImage")
    productPrice = body.get("productPrice")
    productCost = body.get("productCost")
    productBarcode = body.get("productBarcode")
    productStock = body.get("productStock")

    if not all([productName, productPrice]):
        return jsonify({ "message": "Product name and price are required." }), 400

    # TO-DO
    # check if a product with the productName or barcode already exists in user's dashboard

    try:
        new_product = Product(
            dashboardId=dashboard.id,
            productName=productName,
            productImage=productImage,
            productPrice=productPrice,
            productCost=productCost,
            productBarcode=productBarcode,
            productStock=productStock
        )

        new_product.dashboard = dashboard

        db.session.add(new_product)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return jsonify({ "message": "Error creating product" }), 500

    return jsonify({ "message": "Product registered successfully!", "newProduct": new_product.serialize() }), 201
#endregion

#region read product
@product_bp.route("/", methods=["GET"])
@jwt_required()
def get_products():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({ "message": "User not found" }), 404
    
    dashboard = user.dashboard
    if not dashboard:
        return jsonify({ "message": "Couldn't find dashboard for this user" }), 404

    try:
        return jsonify({ "products": [product.serialize() for product in dashboard.products] }), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({ "message": "Error retrieving all dashboard products" }), 500
    
@product_bp.route("/<int:product_id", methods=["GET"])
def get_product(product_id: int):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({ "message": "Product not found" }), 404
    return jsonify({ "product": product.serialize() }), 200
#endregion

#region delete
@product_bp.route("/<int:product_id>", methods=["DELETE"])
@jwt_required()
def delete_product(product_id: int):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({ "message": "Product not found" }), 404
    
    try:
        db.session.delete(product)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return jsonify({ "message": "Error deleting product" }), 500
    
    return jsonify({ "message": "Product deleted successfully!" }), 200
#endregion
