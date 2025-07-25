from flask import Blueprint, request, abort, jsonify
from app.extensions import db
from app.models import Dashboard, User
# from sqlalchemy import or_, func

dashboard_bp = Blueprint("dashboard_bp", __name__)

#region CREATE
@dashboard_bp.route("/", methods=["POST"])
def create_dashboard():
    body = request.json

    if not body:
        abort(400)

    username = body.get("username")
    password = body.get("password")
    dashboard_name = body.get("dashboard_name")

    if not all([username, dashboard_name, password]):
        abort(400)

    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)

    if user.check_password(password) is False:
        abort(403)

    dashboard = Dashboard(user_id=user.id, dashboard_name=dashboard_name)
    
    if Dashboard.query.filter_by(user_id=user.id).first():
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
    dashboard = Dashboard.query.filter_by(id=dashboard_id).first()
    if not dashboard:
        abort(404)
    return jsonify({ "dashboard": dashboard.serialize() }), 200

@dashboard_bp.route("/by-user-id/<int:user_id>", methods=["GET"])
def get_dashboard_by_user_id(user_id: int):
    dashboard = Dashboard.query.filter_by(user_id=user_id).first()
    if not dashboard:
        abort(404)
    return jsonify({ "dashboard": dashboard.serialize() }), 200

@dashboard_bp.route("/by-username/<string:username>", methods=["GET"])
def get_dashboard_by_username(username: str):
    user = User.query.filter_by(username=username).first()
    
    if not user:
        abort(404)

    dashboard = Dashboard.query.filter_by(user_id=user.id).first()
    if not dashboard:
        abort(404)

    return jsonify({ "dashboard": dashboard.serialize() }), 200
#endregion

#region UPDATE
@dashboard_bp.route("/", methods=["UPDATE"])
def update_dashboard():
    body = request.json

    if not body:
        abort(400)

    username = body.get("username")
    password = body.get("password")
    updates = body.get("updates")

    if not all([username, updates, password]):
        abort(400)

    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)
    
    if user.check_password(password) is False:
        abort(403)

    dashboard = Dashboard.query.filter_by(username=username).first()
    if not dashboard:
        abort(404)

    allowed_updates = ["dashboard_name"] # so much changes i know

    for update in updates:
        for key, value in update.items():
            if key in allowed_updates:
                setattr(dashboard, key, value)
    
    try:
        db.session.commit()
    except Exception as e:
        print(f"Error: {str(e)}")
        abort(500)
    
    return jsonify({ "updated_dashboard": dashboard.serialize() }), 200
#endregion

#region DELETE
@dashboard_bp.route("/", methods=["DELETE"])
def delete_dashboard():
    body = request.json

    if not body:
        abort(400)

    username = body.get("username")
    password = body.get("password")

    if not all([username, password]):
        abort(400)

    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)

    if user.check_password(password) is False:
        abort(403)
    
    dashboard = Dashboard.query.filter_by(user_id=user.id).first()
    if not dashboard:
        abort(404)

    try:
        db.session.delete(dashboard)
        db.session.commit()
    except Exception as e:
        print(f"Error: {str(e)}")
        abort(500)
    
    return jsonify({ "deleted_dashboard": dashboard.serialize() }), 200
#endregion
