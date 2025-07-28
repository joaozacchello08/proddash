from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import User, Dashboard, TokenBlocklist
from sqlalchemy import or_
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from dateutil import relativedelta

user_bp = Blueprint("user_bp", __name__)

#region create user
@user_bp.route("/", methods=["POST"])
def create_user():
    body = request.json

    if not body:
        return jsonify({ "message": "No JSON found on request." }), 400
    
    email = body.get("email").replace(" ", "")
    username = body.get("username").replace(" ", "")
    password = body.get("password")
    firstName = body.get("firstName")
    lastName = body.get("lastName")

    if not all([email, username, password]):
        print("Missing required credentials.")
        return jsonify({ "message": "Missing required credentials." }), 400

    if User.query.filter(or_(User.username == username, User.email == email)).first():
        return jsonify({ "message": "User already exists" }), 409

    try:
        new_user = User(
            email=email,
            username=username,
            password=password,
            firstName=firstName,
            lastName=lastName
        )

        new_dashboard = Dashboard(
            userId=None, # will be set automatically by the relationship
            dashboardName=f"{username}'s Dashboard"
        )

        new_user.dashboard = new_dashboard # establishing the relationship

        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({ "message": "Error creating user." }), 500
    
    access_token = create_access_token(
        identity=new_user.id,
        # expires_delta=relativedelta(months=3)
    )

    return jsonify({
        "message": "User created successfully!", 
        "createdUser": new_user.serialize(),
        "accessToken": access_token
    }), 201
#endregion

#region login user
@user_bp.route("/login", methods=["POST"])
def login():
    body = request.json

    if not body:
        return jsonify({ "message": "No JSON found on request." }), 400

    identifier = body.get("identifier")
    password = body.get("password")

    if not all([identifier, password]):
        return jsonify({ "message": "Missing required credentials." }), 400

    user = User.query.filter(or_(User.username == identifier, User.email == identifier)).first()

    if not user:
        return jsonify({ "message": "User not found." }), 404

    if user.check_password(password) is False:
        return jsonify({ "message": "Unauthorized." }), 403

    access_token = create_access_token(
        identity=user.id,
        # expires_delta=relativedelta(months=3)
    )

    return jsonify({ "accessToken": access_token }), 200
#endregion

#region update user data
@user_bp.route("/", methods=["PUT"])
@jwt_required()
def update_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({ "message": "User not found." }), 404
    
    body = request.json
    if not body:
        return jsonify({ "message": "No JSON found on request." }), 400

    if "password" in body:
        user.set_password(body["password"])
        jti = get_jwt()["jti"]
        db.session.add(TokenBlocklist(jti=jti))

    user.username  = body.get("username", user.username)
    user.email     = body.get("email", user.email)
    user.firstName = body.get("firstName", user.firstName)
    user.lastName  = body.get("lastName", user.lastName)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return jsonify({ "message": "Error updating user." }), 500
    
    return jsonify({ "message": "User updated successfully!", "updatedUser": user.serialize() }), 200
#endregion

#region logout user
@user_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    db.session.add(TokenBlocklist(jti=jti))
    db.session.commit()
    return jsonify({ "message": "Successfully logged out." }), 200
#endregion
