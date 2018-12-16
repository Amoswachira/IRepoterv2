import datetime
from flask import Flask, Blueprint
from .api.v2 import VERSION_TWO as v2
from flask_jwt_extended import(JWTManager, jwt_required, create_access_token)
from flask_heroku import Heroku





def create_app():
    app = Flask(__name__)
    app.register_blueprint(v2)
    app.config['JWT_SECRET_KEY'] = 'make nakuru trap again'
    jwt = JWTManager(app)
    heroku = Heroku(app)
    return app
