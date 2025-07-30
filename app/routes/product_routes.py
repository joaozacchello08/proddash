from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Product, User

product_bp = Blueprint("product_bp", __name__)

#region create product
@product_bp.route("/", methods=["POST"])
@jwt_required()
def create_product():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    
    if not user or not user.dashboard:
        return jsonify({ "message": "User or dashboard not found." }), 404

    body = request.json
    if not body:
        return jsonify({ "message": "No JSON found on request." }), 400

    name     = body.get("productName")
    price    = body.get("productPrice")
    cost     = body.get("productCost")
    stock    = body.get("productStock", 0)
    barcode  = body.get("productBarcode")
    image    = body.get("productImage")

    if not all([name, price]):
        return jsonify({ "message": "Missing required fields." }), 400

    try:
        new_product = Product(
            dashboardId    = user.dashboard.id,
            productName    = name,
            productPrice   = price,
            productCost    = cost,
            productStock   = stock,
            productBarcode = barcode,
            productImage   = image
        )

        db.session.add(new_product)
        db.session.commit()

        return jsonify({ "message": "Product created!", "product": new_product.serialize() }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return jsonify({ "message": "Error creating product." }), 500
#endregion

#region get all products
@product_bp.route("/", methods=["GET"])
@jwt_required()
def get_products():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if not user or not user.dashboard:
        return jsonify({ "message": "User or dashboard not found." }), 404

    products = Product.query.filter_by(dashboardId=user.dashboard.id).all()
    return jsonify([product.serialize() for product in products]), 200

@product_bp.route("/<int:product_id>", methods=["GET"])
@jwt_required()
def get_product(product_id: int):
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if not user or not user.dashboard:
        return jsonify({ "message": "User or dashboard not found." }), 404

    product = Product.query.filter_by(dashboardId=user.dashboard.id, id=product_id).first()
    return jsonify({ "product": product.serialize() }), 200

#endregion

#region update product
@product_bp.route("/<int:product_id>", methods=["PUT"])
@jwt_required()
def update_product(product_id: int):
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if not user or not user.dashboard:
        return jsonify({ "message": "User or dashboard not found." }), 404

    product = Product.query.filter_by(id=product_id, dashboardId=user.dashboard.id).first()
    if not product:
        return jsonify({ "message": "Product not found." }), 404

    body = request.json
    if not body:
        return jsonify({ "message": "No JSON found on request." }), 400

    product.productName    = body.get("productName", product.productName)
    product.productPrice   = body.get("productPrice", product.productPrice)
    product.productCost    = body.get("productCost", product.productCost)
    product.productBarcode = body.get("productBarcode", product.productBarcode)
    product.productStock   = body.get("productStock", product.productStock)
    product.productImage   = body.get("productImage", product.productImage)

    try:
        db.session.commit()
        return jsonify({ "message": "Product updated.", "product": product.serialize() }), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return jsonify({ "message": "Error updating product." }), 500
#endregion

#region delete product
@product_bp.route("/<int:product_id>", methods=["DELETE"])
@jwt_required()
def delete_product(product_id: int):
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if not user or not user.dashboard:
        return jsonify({ "message": "User or dashboard not found." }), 404

    product = Product.query.filter_by(id=product_id, dashboardId=user.dashboard.id).first()
    if not product:
        return jsonify({ "message": "Product not found." }), 404

    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({ "message": "Product deleted successfully." }), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return jsonify({ "message": "Error deleting product." }), 500
#endregion
