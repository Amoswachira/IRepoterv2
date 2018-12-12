from flask_restful import Api, Resource
from flask import Blueprint

version_two = Blueprint('api_v2', __name__, url_prefix='/api/v2')
api = Api(version_two)
