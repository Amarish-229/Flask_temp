from os import access
from flask import Blueprint, app, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from src.database import User, db
import validators
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flasgger import swag_from


auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

@auth.post('/register')
@swag_from('../docs/auth/register.yaml')
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if len(password) < 6:
        return jsonify({'error': "Password is too short"}), HTTP_400_BAD_REQUEST

    if len(username) < 3:
        return jsonify({'error': "Username is too short"}), HTTP_400_BAD_REQUEST

    if not username.isalnum() or " " in username:
        return jsonify({'error': "Username should be alphanumeric, also no spaces"}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error': "Email is not valid"}), HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': "Email is taken"}), HTTP_409_CONFLICT

    

    pwd_hash = generate_password_hash(password)
    user_id = User.generate_userid()
    user = User(id=user_id,username=username, password=pwd_hash, email=email)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': "User created",
        'user': {
            'username': username, "email": email
        }

    }), HTTP_201_CREATED



@auth.post('/login')
@swag_from("../docs/auth/login.yaml")
def login():
    json_data = request.get_json()
    email = json_data.get('email', '')
    password = json_data.get('password', '')

    if not email: return {"message":"email id is required"}, HTTP_400_BAD_REQUEST
    if not password: return {"message":"password is missing"}, HTTP_400_BAD_REQUEST

    user = User.query.filter_by(email=email).first()

    if not user: return {"message": "You are not registered with us"}, HTTP_404_NOT_FOUND

    if not check_password_hash(user.password, password):
        return {"message": "password does not match"}, HTTP_401_UNAUTHORIZED
    
    access = create_access_token(identity=user.id)
    refresh = create_refresh_token(identity=user.id)
    return jsonify({
        "message": "Ok",
        "user": {
        "access": access,
        "refresh": refresh,
        "username": user.username,
        "email": user.email
        }
    }), HTTP_200_OK


@auth.get("/token/refresh")
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({
        'access': access
    }), HTTP_200_OK