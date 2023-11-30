from flask import Flask, Blueprint
from flask_restful import Api
from src.Admin.routes import admin_routes
from src.Dashboard.routes import routes
from src.User.routes import create_authentication_routes
from src.UOT.routes import UOT_routes
from src.Tutorial.routes import Tutorial_routes

class RouteInitialization:
    def __init__(self):
        self.blueprints = [
            {
                "name": "auth", 
                "blueprint": Blueprint('auth', __name__, static_url_path="assets"), 
                "register_callback": create_authentication_routes, 
                "url_prefix": "/"
            },
            {
                "name": "bp", 
                "blueprint": Blueprint('api', __name__, static_url_path="assets"), 
                "register_callback": routes, 
                "url_prefix": "/api/v1"
            },
            {
                "name": "admin_bp", 
                "blueprint":  Blueprint('admin', __name__, static_url_path="assets"), 
                "register_callback": admin_routes, 
                "url_prefix": "/api/v1/admin"
            },
            {
                "name": "UOT", 
                "blueprint":  Blueprint('UOT', __name__, static_url_path="assets"), 
                "register_callback": UOT_routes, 
                "url_prefix": "/api/v1"
            },
            {
                "name": "training", 
                "blueprint":  Blueprint('Training', __name__, static_url_path="assets"), 
                "register_callback": Tutorial_routes, 
                "url_prefix": "/api/v1"
            },
        ]


    def init_app(self, flask_app: Flask):
        for blueprint in self.blueprints:
            init_route = Api(blueprint.get("blueprint"))
            blueprint.get("register_callback")(init_route)
            flask_app.register_blueprint(blueprint.get("blueprint"), url_prefix=blueprint.get("url_prefix"))
