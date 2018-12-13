from flask import Flask, Blueprint
from .api.v2 import version_two as v2
from flask_jwt_extended import(JWTManager, jwt_required, create_access_token)


def create_app():
    app = Flask(__name__)
    app.register_blueprint(v2)
    app.config['JWT_SECRET_KEY'] = 'make nakuru trap again'
    jwt = JWTManager(app)
    return app
