"""define all routes: api endpoints"""
from flask_restful import Api, Resource
from flask import Blueprint
from flask_jwt_extended.exceptions import *
from .views import Interventions, AdminUpdatesInterventiontatus, Intervention, AdminupdateRedflagstatus, Updatelocation, Updatecomment
from .users import Signup, Login, Users, AdminIncidents

VERSION_TWO = Blueprint('api_v2', __name__, url_prefix='/api/v2')
API = Api(VERSION_TWO, catch_all_404s=True)


API.add_resource(Updatelocation,
                 '/interventions/<int:intervention_id>/location')
API.add_resource(Updatecomment, '/interventions/<int:intervention_id>/comment')
API.add_resource(Signup, '/auth/signup')
API.add_resource(AdminUpdatesInterventiontatus,
                 '/interventions/<int:intervention_id>/status')
API.add_resource(AdminupdateRedflagstatus,
                 '/redflag/<int:intervention_id>/status')
API.add_resource(Interventions, '/interventions')
API.add_resource(Intervention, '/intervention/<int:intervention_id>')
API.add_resource(Login, '/auth/login')
API.add_resource(Users, '/users')
API.add_resource(AdminIncidents, '/Incidents')
