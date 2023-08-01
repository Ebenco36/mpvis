from functools import wraps
import jwt, json
from flask import request, abort
from flask import current_app
from src.User.model import UserModel

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            data=jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            print(data)
            current_user=UserModel.query.filter_by(id = data["id"]).first()
            print(current_user)
            if current_user is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
            if not current_user.status:
                abort(403)
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500
        data = {
            'id': current_user.id,
            'name': current_user.name,
            'username': current_user.username,
            'email': current_user.email,
            'phone': current_user.phone,
        }
        return f(*args, **kwargs)

    return decorated