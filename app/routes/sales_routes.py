from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import User, Product, Venda
from flask_jwt_extended import get_jwt_identity, jwt_required

sales_bp = Blueprint("sales_bp", __name__)


#region register
@sales_bp.route("/<int:product_id>", methods=["POST"])
@jwt_required()
def register_sale(product_id: int):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({ "message": "User not found." }, 404)

    body = request.json
    if not body:
        return jsonify({ "message": "No JSON found on request." }), 400

    sold_amount = body.get("soldAmount")
    price_at_sale = body.get("priceAtSale")

    if not sold_amount:
        return jsonify({ "message": "soldAmount is required." }), 400

    try:
        product = Product.query.filter_by(id=product_id, dashboardId=user.dashboard.id).first()
        if not product:
            return jsonify({ "message": "Product not found on this dashboard" }), 404

        if sold_amount > product.productStock:
            return jsonify({ "message": "Sold amount is more than actual stock." }), 400

        _price_at_sale = price_at_sale if price_at_sale else product.priceAtSale
        cost_at_sale = product.costAtSale

        new_sale = Venda(
            productId=product_id,
            dashboardId=product.dashboardId,
            soldAmount=int(sold_amount),
            priceAtSale=float(_price_at_sale),
            costAtSale=float(cost_at_sale)
        )

        product.productStock -= int(sold_amount)

        db.session.add(new_sale)
        db.session.commit()
    except Exception as e:
        print(f"Error: {str(e)}")
        db.session.rollback()
        return jsonify({ "message": "Error trying to register sale." }), 500
    
    return jsonify({ "message": "Sale registered successfully!", "newSale": new_sale.serialize() }), 201
#endregion

#region load sales
@sales_bp.route("/<int:venda_id>", methods=["GET"])
@jwt_required()
def get_venda(venda_id: int):
    venda = Venda.query.get(venda_id)
    if not venda:
        return jsonify({ "message": "Sale not found" }), 404
    return jsonify({ "sale": venda.serialize() }), 200

@sales_bp.route("/", methods=["GET"])
@jwt_required()
def get_vendas():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({ "message": "User not found." }), 404
    
    sales = user.dashboard.sales
    
    try:
        return jsonify({ "sales": [sale.serialize() for sale in sales] }), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({ "message": "Error retrieving sales." }), 500
#endregion

#region update sale
@sales_bp.route("/<int:sale_id>", methods=["PUT"])
@jwt_required()
def update_sale(sale_id: int):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({ "message": "User not found." }), 404
    
    body = request.json
    if not body:
        return jsonify({ "message": "No JSON found on request." }), 400
    
    dashboard = user.dashboard
    if not dashboard:
        return jsonify({ "message": "No dashboard found for this user." }), 404
    
    sale = Venda.query.filter_by(id=sale_id, dashboardId=dashboard.id).first()

    if not sale:
        return jsonify({ "message": "Sale not found." }), 404

    sale.soldAmount = body.get("soldAmount", sale.soldAmount)
    sale.priceAtSale = body.get("priceAtSale", sale.priceAtSale)
    sale.costAtSale = body.get("costAtSale", sale.costAtSale)
    sale.soldAt = body.get("soldAt", sale.soldAt)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return jsonify({ "message": "Error updating sale." }), 500
    
    return jsonify({ "message": "Sale updated successfully." }), 200
        
#endregion

#region delete sale
@sales_bp.route("/<int:sale_id>", methods=["DELETE"])
@jwt_required()
def delete_user(sale_id: int):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({ "message": "User not found." }), 404

    dashboard = user.dashboard
    if not dashboard:
        return jsonify({ "message": "Dashboard not found for this user." }), 404

    try:
        sale = Venda.query.filter_by(id=sale_id, dashboardId=dashboard.id).first()

        if not sale:
            return jsonify({ "message": "Sale not found or you don't have permission to delete it." }), 404
        
        product = Product.query.get(sale.productId)
        if product:
            product.productStock += sale.soldAmount

        db.session.delete(sale)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return jsonify({ "message": "Error deleting sale." }), 500
    
    return jsonify({ "message": "Sale deleted successfully." }), 200
#endregion
