from flask import Blueprint, request, abort, jsonify
from app.extensions import db
from app.models import Dashboard
# from sqlalchemy import or_, func

dashboard_bp = Blueprint("dashboard_bp", __name__)

#region CREATE
@dashboard_bp.route("/", methods=["POST"])
def create_dashboard():
    body = request.json

    if not body:
        abort(400)

    user_id = body.get("user_id")
    dashboard_name = body.get("dashboard_name")

    if not all([user_id, dashboard_name]):
        abort(400)

    dashboard = Dashboard(user_id=user_id, dashboard_name=dashboard_name)
    
    if Dashboard.query.filter_by(user_id=user_id).first():
        abort(409)
    
    try:
        db.session.add(dashboard)
        db.session.commit()
    except Exception as e:
        print(f"Error: {str(e)}")
        abort(500)

    return jsonify({ "message": "Dashboard created successfully!", "created_dashboard": dashboard.serialize() }), 201
#endregion

#region READ
@dashboard_bp.route("/<int:dashboard_id>", methods=["GET"])
def get_dashboard(dashboard_id: int):
    dashboard = Dashboard.query.filter_by(dashboard_id).first()
    if not dashboard:
        abort(404)
    return jsonify({ "dashboard": dashboard.serialize() }), 200

@dashboard_bp.route("/by-user/<int:user_id>", methods=["GET"])
def get_dashboard_by_user_id(user_id: int):
    dashboard = Dashboard.query.filter_by(user_id=user_id).first()
    if not dashboard:
        abort(404)
    return jsonify({ "dashboard": dashboard.serialize() }), 200
#endregion
