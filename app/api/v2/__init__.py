from flask_restful import Api, Resource
from flask import Blueprint
from .views import Interventions, AdminUpdatesInterventiontatus, Intervention, AdminupdateRedflagstatus, Updatelocation, Updatecomment

version_two = Blueprint('api_v2', __name__, url_prefix='/api/v2')
api = Api(version_two)
api.add_resource(Updatelocation,
                 '/interventions/<int:intervention_id>/location')
api.add_resource(Updatecomment, '/interventions/<int:intervention_id>/comment')
api.add_resource(AdminUpdatesInterventiontatus,
                 '/interventions/<int:intervention_id>/status')
api.add_resource(AdminupdateRedflagstatus,
                 '/interventions/<int:intervention_id>/status-red')
api.add_resource(Interventions, '/interventions')
api.add_resource(Intervention, '/intervention/<int:intervention_id>')
