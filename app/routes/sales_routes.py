from flask import Blueprint, request, abort, jsonify
from app.extensions import db
from app.models import Dashboard, Product, Venda

sales_bp = Blueprint("sales_bp", __name__)


#region register
@sales_bp.route("/", methods=["POST"])
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
            productId=product_id,
            dashboardId=product.dashboard_id,
            soldAmount=int(sold_amount),
            priceAtSale=float(_price_at_sale),
            costAtSale=float(cost_at_sale)
        )

        product.product_stock -= int(sold_amount)

        db.session.add(new_sale)
        db.session.commit()
    except Exception as e:
        print(f"Error: {str(e)}")
        abort(500)
    
    return jsonify({ "message": "Sale registered successfully!", "newSale": new_sale.serialize() }), 201
#endregion

#region load sales
@sales_bp.route("/<int:venda_id>", methods=["GET"])
def get_venda(venda_id: int):
    venda = db.session.get(Venda, venda_id)
    if not venda:
        abort(404)
    return jsonify({ "sale": venda.serialize() }), 200

# load sales from a dashboard
@sales_bp.route("/dashboard/<int:dashboard_id>", methods=["GET"])
def get_vendas(dashboard_id: int):
    dashboard = db.session.get(Dashboard, dashboard_id)
    if not dashboard:
        abort(404)

    return jsonify({ "sales": [sale.serialize() for sale in dashboard.sales] }), 200
#endregion

#region delete sales
@sales_bp.route("/", methods=["DELETE"])
def delete_user():
    pass
#endregion

