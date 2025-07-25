from flask import Blueprint, request, abort, jsonify
from app.extensions import db
from app.models import User
from sqlalchemy import or_, func

user_bp = Blueprint("user_bp", __name__)

#region CREATE
@user_bp.route("/", methods=["POST"])
def create_user():
    body = request.json

    if not body:
        abort(400)
    
    email = body.get("email")
    password = body.get("password")
    username = body.get("username")
    first_name = body.get("first_name")
    last_name = body.get("last_name")

    if not all([email, username, password]):
        abort(400)

    if User.query.filter(or_(User.username == username, User.email == email)).first():
        abort(409)

    # new user
    user = User(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )

    try:
        db.session.add(user)
        db.session.commit() 
    except Exception as e:
        print(f"Error: {e}")
        abort(500)

    return jsonify({ "message": "User created successfully!", "createdUser": user.serialize() }), 201
#endregion

#region READ
@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id: int):
    user = User.query.filter_by(id=user_id).first()
    
    if not user:
        abort(404)

    return jsonify({ "user": user.serialize() }), 200

@user_bp.route("/", methods=["GET"])
def get_random_user():
    random_user = User.query.order_by(func.random()).first()
    
    if not random_user:
        abort(404)

    return jsonify({ "random_user": random_user.serialize() }), 200

@user_bp.route("/login", methods=["POST"])
def login_user():
    body = request.json

    if not body:
        abort(400)

    email = body.get("email")
    password = body.get("password")

    if not all([email, password]):
        abort(400)

    user = User.query.filter_by(email=email).first()
    if not user:
        abort(404)

    if user.check_password(password) is False:
        abort(403)
    
    return jsonify({ "message": "User logged in." }), 200
#endregion

#region UPDATE
@user_bp.route("/", methods=["UPDATE"])
def update_user():
    body = request.json

    if not body:
        abort(400)

    email = body.get("email")
    # username = body.get("username")
    password = body.get("password")
    updates = body.get("updates")

    if not all([email, password]):
        abort(400)

    user = User.query.filter_by(email=email).first()

    if not user:
        abort(404)

    if user.check_password(password) is False:
        abort(403)
    
    allowed_updates = ["username", "first_name", "last_name"]

    for update in updates:
        for key, value in update.items():
            if key in allowed_updates:
                setattr(user, key, value)
    
    try:
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

    email = body.get("email")
    password = body.get("password")

    if not all([email, password]):
        abort(400)

    user = User.query.filter_by(email=email).first()
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
