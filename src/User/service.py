import json
import jwt
import datetime
from os import environ
from database.db import db
from sqlalchemy import or_
from flask import g, jsonify
from src.User.helper import send_forgot_password_email
from src.User.model import UserModel
from src.middlewares.auth_middleware import token_required
from src.utils.common import generate_response, TokenGenerator
from src.User.validation import (
    CreateLoginInputSchema,
    CreateResetPasswordEmailSendInputSchema,
    CreateSignupInputSchema, ResetPasswordInputSchema,
)
from src.utils.http_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus

def create_user(request, input_data):
    """
    It creates a new user
    :param request: The request object
    :param input_data: This is the data that is passed to the function
    :return: A response object
    """
    # Validate input_data using a schema (replace 'YourValidationSchema' with the actual schema class)
    create_validation_schema = CreateSignupInputSchema()
    errors = create_validation_schema.validate(input_data)
    print(errors)
    if errors:
        return generate_response(message=errors, status=HTTPStatus.BAD_REQUEST)

    # Check if username or email already exists
    check_username_exist = UserModel.query.filter_by(username=input_data.get("username")).first()
    check_email_exist = UserModel.query.filter_by(email=input_data.get("email")).first()
    print(check_email_exist)
    if check_username_exist:
        return generate_response(message="Username already exists", status=HTTPStatus.BAD_REQUEST)
    elif check_email_exist:
        return generate_response(message="Email already taken", status=HTTPStatus.BAD_REQUEST)

    # Create a new user instance
    new_user = UserModel(**input_data)
    new_user.password = generate_password_hash(input_data.get("password"), method='sha256')
    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    # Response data without the password
    del input_data["password"]
    return generate_response(data=input_data, message="Registration successful", status=HTTPStatus.CREATED)


def login_user(request, input_data):
    """
    It takes in a request and input data, validates the input data, checks if the user exists, checks if
    the password is correct, and returns a response
    :param request: The request object
    :param input_data: The data that is passed to the function
    :return: A dictionary with the keys: data, message, status
    """
    # Validate input_data using a schema (replace 'YourValidationSchema' with the actual schema class)
    create_validation_schema = CreateLoginInputSchema()
    errors = create_validation_schema.validate(input_data)

    if errors:
        current_app.logger.info(errors)
        return generate_response(message=errors, status=HTTPStatus.BAD_REQUEST)

    email_or_username = input_data.get("email")
    print("Where we are: "+email_or_username)
    # Use 'filter' instead of 'filter_by' and 'or_' to create an OR condition
    get_user = UserModel.query.filter(
        (UserModel.email == email_or_username) | (UserModel.username == email_or_username)
    ).first()

    current_app.logger.info(get_user)

    if get_user is None:
        return generate_response(message="User not found", status=HTTPStatus.BAD_REQUEST)
    # check password 
    if check_password_hash(get_user.password, input_data.get("password")):
        token = jwt.encode(
            {
                "id": get_user.id,
                "email": get_user.email,
                "username": get_user.username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            },
            current_app.config["SECRET_KEY"],
        )
        input_data["token"] = token
        return generate_response(
            data=input_data, message="User login successfully", status=HTTPStatus.CREATED
        )
    else:
        return generate_response(message="Password is wrong", status=HTTPStatus.BAD_REQUEST)
    
    
def reset_password_email_send(request, input_data):
    """
    It takes an email address as input, checks if the email address is registered in the database, and
    if it is, sends a password reset email to that address
    :param request: The request object
    :param input_data: The data that is passed to the function
    :return: A response object with a message and status code.
    """
    create_validation_schema = CreateResetPasswordEmailSendInputSchema()
    errors = create_validation_schema.validate(input_data)
    if errors:
        return generate_response(message=errors)
    user = UserModel.query.filter_by(email=input_data.get("email")).first()
    if user is None:
        return generate_response(
            message="No record found with this email. please signup first.",
            status=HTTP_400_BAD_REQUEST,
        )
    send_forgot_password_email(request, user)
    return generate_response(
        message="Link sent to the registered email address.", status=HTTP_200_OK
    )


def reset_password(request, input_data, token):
    create_validation_schema = ResetPasswordInputSchema()
    errors = create_validation_schema.validate(input_data)
    if errors:
        return generate_response(message=errors)
    if not token:
        return generate_response(
            message="Token is required!",
            status=HTTP_400_BAD_REQUEST,
        )
    token = TokenGenerator.decode_token(token)
    user = UserModel.query.filter_by(id=token.get('id')).first()
    if user is None:
        return generate_response(
            message="No record found with this email. please signup first.",
            status=HTTP_400_BAD_REQUEST,
        )
    user = UserModel.query.filter_by(id=token['id']).first()
    user.password = generate_password_hash(input_data.get('password')).decode("utf8")
    db.session.commit()
    return generate_response(
        message="New password SuccessFully set.", status=HTTP_200_OK
    )


def current_user():
    if g.current_user:
        return {
            "name": g.current_user.name,
            "email": g.current_user.email,
            "username": g.current_user.username,
            "phone": g.current_user.phone,
        }, 200
    else:
        return {'message': 'Unauthorized'}, 401
    
class UserService:
    @staticmethod
    def get_all_users():
        return UserModel.query.all()

    @staticmethod
    def create_user(name, phone, username, email, password, status=True, is_admin=False):
        new_user = UserModel(
            name = name,
            email = email,
            phone = phone,
            username = username, 
            is_admin = is_admin
        )
        if(password):
            new_user.password = generate_password_hash(password, method='sha256')
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def get_user_by_id(user_id):
        return UserModel.query.get(user_id)

    @staticmethod
    def update_user(user_id, name=None, phone=None, status=True, username=None, email=None, is_admin=False):
        user = UserModel.query.filter_by(id=user_id).first()
        if(username):
            user.username = username
        if(email):
            user.email = email
        if(is_admin):
            user.is_admin = is_admin
        if(name):
            user.name = name
        if(phone):
            user.phone = phone
        if(status):
            user.status = status
        db.session.commit()

    @staticmethod
    def delete_user(user_id):
        user = UserModel.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()