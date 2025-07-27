from flask import Blueprint, request, abort, jsonify
from app.extensions import db
from app.models import User, Dashboard
from sqlalchemy import or_, func

user_bp = Blueprint("user_bp", __name__)

#region CREATE
@user_bp.route("/", methods=["POST"])
def create_user():
    body = request.json

    if not body:
        abort(400)
    
    email = body.get("email")
    username = body.get("username")
    password = body.get("password")
    first_name = body.get("firstName")
    last_name = body.get("lastName")

    if not all([email, username, password]):
        abort(400)

    if User.query.filter(or_(User.username == username, User.email == email)).first():
        abort(409)

    try:
        new_user = User(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        new_dashboard = Dashboard(
            user_id=None, # will be set automatically by the relationship
            dashboard_name=f"{username}'s Dashboard"
        )

        new_user.dashboard = new_dashboard # establishing the relationship

        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        print(f"Error: {e}")
        abort(500)

    return jsonify({ "message": "User created successfully!", "createdUser": new_user.serialize() }), 201
#endregion

#region READ
@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id: int):
    user = db.session.get(User, user_id)
    if not user:
        abort(404)
    return jsonify({ "user": user.serialize() }), 200

@user_bp.route("/random", methods=["GET"])
def get_random_user():
    random_user = User.query.order_by(func.random()).first()
    
    if not random_user:
        abort(404)

    return jsonify({ "random_user": random_user.serialize() }), 200

@user_bp.route("/by-username/<string:username>", methods=["GET"])
def get_user_by_username(username: str):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)
    return jsonify({ "user": user.serialize() }), 200
#endregion

#region UPDATE
@user_bp.route("/", methods=["UPDATE"])
def update_user():
    body = request.json

    if not body:
        abort(400)

    # email = body.get("email")
    username = body.get("username")
    password = body.get("password")
    updates = body.get("updates")

    if not all([username, password]):
        abort(400)

    user = db.session.query(User).filter_by(username=username).first()

    if not user:
        abort(404)

    if user.check_password(password) is False:
        abort(403)
    
    allowed_updates = ["first_name", "last_name"]
    
    try:
        for update in updates:
            for key, value in update.items():
                if key in allowed_updates:
                    setattr(user, key, value)

        db.session.commit()
    except Exception as e:
        print(f"Error: {str(e)}")
        abort(500)

    return jsonify({ "message": "User updated successfully!", "updated_user": user.serialize() }), 200
#endregion

#region DELETE
@user_bp.route("/", methods=["DELETE"])
def delete_user():
    body = request.json

    if not body:
        abort(400)

    username = body.get("email")
    password = body.get("password")

    if not all([username, password]):
        abort(400)

    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)

    if user.check_password(password) is False:
        abort(403)

    try:
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        print(f"Error: {str(e)}")
        abort(500)

    return jsonify({ "message": "User deleted successfully.", "deleted_user": user.serialize() }), 200
#endregion
