from flask import Flask, Blueprint
from .api.v2 import version_two as v2


def create_app():
    app = Flask(__name__)
    app.register_blueprint(v2)
    return app
