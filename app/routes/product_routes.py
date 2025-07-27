from flask import Blueprint, request, abort, jsonify
from app.extensions import db
from app.models import User, Dashboard, Product, Venda
from sqlalchemy import or_#, func

product_bp = Blueprint("product_bp", __name__)

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
        
        if Product.query.filter_by(dashboard_id=dashboard_id, product_name=product_name).first() or Product.query.filter_by(dashboard_id=dashboard_id, product_barcode=product_barcode).first():
            abort(409)
        
        new_product = Product(
            product_name=product_name,
            product_price=float(product_price),
            product_stock=int(product_stock),
            product_image=product_image,
            product_barcode=product_barcode,
            product_cost=float(product_cost) if product_cost is not None else None
        )

        new_product.dashboard = dashboard

        db.session.add(new_product)
        db.session.commit()
    except Exception as e:
        print(f"Error: {str(e)}")
        abort(500)
    
    return jsonify({ "message": "Product created successfully!", "newProduct": new_product.serialize() }), 201
#endregion

#region vendas
## register
@product_bp.route("/sales", methods=["POST"])
def register_sale():
    body = request.json

    if not body:
        abort(400)

    product_id = body.get("productId")
    sold_amount = body.get("soldAmount")
    price_at_sale = body.get("priceAtSale")

    if not product_id:
        abort(400)

    try:
        product = db.session.get(Product, product_id)
        if not product:
            abort(404)

        if sold_amount > product.product_stock:
            abort(400)

        _price_at_sale = price_at_sale if price_at_sale else product.price_at_sale
        cost_at_sale = product.cost_at_sale

        new_sale = Venda(
            product_id=product_id,
            dashboard_id=product.dashboard_id,
            sold_amount=int(sold_amount),
            price_at_sale=float(_price_at_sale),
            cost_at_sale=float(cost_at_sale)
        )

        product.product_stock -= int(sold_amount)

        db.session.add(new_sale)
        db.session.commit()
    except Exception as e:
        print(f"Error: {str(e)}")
        abort(500)
    
    return jsonify({ "message": "Sale registered successfully!", "newSale": new_sale.serialize() }), 201

## load sale
@product_bp.route("/sales/<int:venda_id>", methods=["GET"])
def get_venda(venda_id: int):
    venda = db.session.get(Venda, venda_id)
    if not venda:
        abort(404)
    return jsonify({ "sale": venda.serialize() }), 200

## load sales from a dashboard
@product_bp.route("/sales/dashboard/<int:dashboard_id>", methods=["GET"])
def get_vendas(dashboard_id: int):
    dashboard = db.session.get(Dashboard, dashboard_id)
    if not dashboard:
        abort(404)

    return jsonify({ "sales": [sale.serialize() for sale in dashboard.sales] }), 200
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
