from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import User, Dashboard
from flask_jwt_extended import jwt_required, get_jwt_identity

dashboard_bp = Blueprint("dashboard_bp", __name__)

#region create new dashboard
@dashboard_bp.route("/", methods=["POST"])
@jwt_required()
def create_dashboard():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    if not user:
        return jsonify({ "message": "User not found" }), 404
    
    if user.dashboard:
        return jsonify({ "message": "User already have a dashboard." }), 409
    
    body = request.json
    if not body:
        return jsonify({ "message": "No JSON found on request." }), 404

    dashboardName = body.get("dashboardName", f"New {user.username}'s Dashboard")

    try:
        new_dashboard = Dashboard(
            userId=None,
            dashboardName=dashboardName
        )

        user.dashboard = new_dashboard

        db.session.add(new_dashboard)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return jsonify({ "message": "Error creating new dashboard." }), 500
    
    return jsonify({ "message": "Dashboard created successfully!", "createdDashboard": new_dashboard.serialize() }), 201
#endregion

#region read dashboard
@dashboard_bp.route("/<int:dashboard_id>", methods=["GET"])
@jwt_required()
def get_dashboard(dashboard_id: int):
    dashboard = Dashboard.query.get(dashboard_id)
    if not dashboard:
        return jsonify({ "message": "Dashboard not found." }), 404
    return jsonify({ "dashboard": dashboard.serialize() }), 200

@dashboard_bp.route("/", methods=["GET"])
@jwt_required()
def get_dashboard_from_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({ "message": "User not found." }), 404
    dashboard = user.dashboard
    if not dashboard:
        return jsonify({ "message": "Didn't found a dashboard for this user." }), 404
    
    return jsonify({ "dashboard": dashboard.serialize() }), 200
#endregion

#region update dashboard
@dashboard_bp.route("/", methods=["PUT"])
@jwt_required()
def update_dashboard():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    if not user:
        return jsonify({ "message": "User not found." }), 404
    
    dashboard = user.dashboard
    if not dashboard:
        return jsonify({ "message": "Couldn't find a dashboard for this user." }), 404
    
    body = request.json
    if not body:
        return jsonify({ "message": "No JSON found on the request." }), 400
    
    dashboard.dashboardName = body.get("dashboardName", dashboard.dashboardName)

    try:
        db.session.commit()
    except Exception as e:
        print(f"Error: {str(e)}")
        db.session.rollback()
        return jsonify({ "error": "Internal server error updating dashboard." }), 500

    return jsonify({ "message": "Dashboard updated successfully!" }), 200
#endregion

#region delete dashboard
@dashboard_bp.route("/", methods=["DELETE"])
@jwt_required()
def delete_dashboard():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    if not user:
        return jsonify({ "message": "User not found" }), 404
    
    dashboard = user.dashboard
    if not dashboard:
        return jsonify({ "message": "Couldn't find dashboard for this user." }), 404
    
    try:
        db.session.delete(dashboard)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return jsonify({ "message": "Error updating dashboard." }), 500
    
    return jsonify({ "message": "Dashboard updated successfully!" }), 200
#endregion
