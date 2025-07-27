from flask import Blueprint, request, abort, jsonify
from app.extensions import db
from app.models import User, Dashboard
from sqlalchemy import or_, func
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

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

    if not all([username, password]):
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

#region login user
@user_bp.route("/login", methods=["POST"])
def login():
    body = request.json

    if not body:
        abort(400)

    identifier = body.get("identifier")
    password = body.get("password")

    if not all([identifier, password]):
        abort(400)

    user = User.query.filter(or_(User.username == identifier, User.email == identifier)).first()

    if not user:
        abort(404)

    if user.check_password(password) is False:
        abort(403)

    access_token = create_access_token(identity=user.id)

    return jsonify(access_token=access_token)

#endregion
