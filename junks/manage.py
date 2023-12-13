import os
from src.MP import flask_app as app
from src import RouteInitialization

"""
    Route Implementation. Well structured
"""
init_route = RouteInitialization()
init_route.init_app(app)


@app.route('/')
def index():
    return 'Welcome to MPvis Rest API Setup!'


if __name__ == '__main__':
    app.run(debug=True)