from flask import Response
from flask_restful import Resource
from flask import request, make_response
from src.User.service import create_user, reset_password_email_send, login_user, reset_password, current_user, UserService
from src.middlewares.auth_middleware import token_required
from src.User.requests import UserRequest, UserUpdateRequest

class SignUpApi(Resource):
    @staticmethod
    def post() -> Response:
        """
        POST response method for creating user.
        :return: JSON object
        """
        input_data = request.get_json()
        response, status = create_user(request, input_data)
        return make_response(response, status)


class LoginApi(Resource):
    @staticmethod
    def post() -> Response:
        """
        POST response method for login user.
        :return: JSON object
        """
        input_data = request.get_json()
        response, status = login_user(request, input_data)
        return make_response(response, status)


class ForgotPassword(Resource):
    @staticmethod
    def post() -> Response:
        """
        POST response method for forgot password email send user.
        :return: JSON object
        """
        input_data = request.get_json()
        response, status = reset_password_email_send(request, input_data)
        return make_response(response, status)


class ResetPassword(Resource):
    @staticmethod
    def post(token) -> Response:
        """
        POST response method for save new password.
        :return: JSON object
        """
        input_data = request.get_json()
        response, status = reset_password(request, input_data, token)
        return make_response(response, status)
        
class CurrentUserResource(Resource):
    @token_required
    def get(self):
        response, status = current_user()
        return make_response(response, status)
    


class UserResource(Resource):
    @token_required
    def get(self):
        users = UserService.get_all_users()
        user_list = [{
            'id': user.id, 
            'name': user.name, 
            'phone': user.phone, 
            'username': user.username, 
            'email': user.email, 
            'is_admin': user.is_admin
        } for user in users]
        return {'users': user_list, "message": "fetch records successfully."}

    def post(self):
        args = UserRequest.parse_args()
        user = UserService.create_user(
            args['name'], 
            args['phone'], 
            args['username'], 
            args['email'], 
            args['password'], 
            args['status'], 
            args['is_admin']
        )
        return {
            'message': 'User created successfully', 
            'user': {
                'id': user.id, 
                'name': user.name, 
                'phone': user.phone, 
                'username': user.username, 
                'email': user.email, 
                'is_admin': user.is_admin
            }}

class UserDetailResource(Resource):
    @token_required
    def get(self, user_id):
        user = UserService.get_user_by_id(user_id)
        if user:
            return {'user': {
                'id': user.id, 
                'name': user.name, 
                'phone': user.phone, 
                'email': user.email, 
                'username': user.username, 
                'is_admin': user.is_admin
                }
            }
        else:
            return {'message': 'User not found'}, 404
        
    @token_required
    def put(self, user_id):
        args = UserUpdateRequest.parse_args()
        UserService.update_user(
            user_id, 
            args['name'], 
            args['phone'], 
            args['status'], 
            args['username'], 
            args['email'], 
            args['is_admin']
        )
        return {'message': 'User updated successfully'}

    @token_required
    def delete(self, user_id):
        UserService.delete_user(user_id)
        return {'message': 'User deleted successfully'}