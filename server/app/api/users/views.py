# server/app/api/users/views.py

from sqlalchemy import exc
from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token
)
from app import db, bcrypt
from app.api.users.models import User


class UsersRegister(Resource):
    def post(self):
        post_data = request.get_json()
        response_object = {
            "message": "Invalid payload."
        }
        if not post_data:
            return response_object, 400
        email = post_data.get("email")
        password = post_data.get("password")
        name = post_data.get("name")
        try:
            user = User.find(email=email)
            if not user:
                user = User(name=name, email=email, password=password)
                user.insert()
                added_user = User.find(
                    email=post_data["email"]
                )
                response_object = added_user.json()
                return response_object, 201
            else:
                response_object["message"] = (
                    "Sorry. That email already exists."
                )
                return response_object, 400
        except exc.IntegrityError:
            db.session.rollback()
            return response_object, 400
        except (exc.IntegrityError, ValueError, TypeError):
            db.session.rollback()
            return response_object, 400


class UserLogin(Resource):
    def post(self):
        post_data = request.get_json()
        response_object = {
            "message": "Invalid payload."
        }
        if not post_data:
            return response_object, 400
        email = post_data.get("email")
        password = post_data.get("password")
        try:
            user = User.query.filter_by(email=email).first()
            if user:
                valid_password = bcrypt.check_password_hash(
                    user.password_hash,
                    password
                )
                if valid_password:
                    token = create_access_token(
                        identity=user.id.__str__(), fresh=True
                    )
                    response_object = {
                        "token": token
                    }
                    return response_object, 200
            else:
                response_object["message"] = "User does not exist."
                return response_object, 404
        except Exception as e:
            print(e)
            response_object["message"] = "Try again."
            return response_object, 500


class UserLogOut(Resource):
    @jwt_required
    def get(self):
        response_object = {
            "message": "Provide a valid auth token."
            }
        current_user = get_jwt_identity()
        if current_user:
            response_object["message"] = "Successfully logged out."
            return response_object, 200
