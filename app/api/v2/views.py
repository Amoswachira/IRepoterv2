"""views for the intervention contains all methods for get,post and patch"""
from datetime import timedelta
import re
from flask_restful import Resource, reqparse
from flask import jsonify, make_response, request
from flask_jwt_extended import(
    jwt_required, get_jwt_identity)
from .models import Model


EXPIRES = timedelta(minutes=60)
DB = Model()
DB.create_tables()

# validators


def is_valid(value):
    '''check if the string is empty'''
    if not value:
        raise ValueError("empty string")


def valid_characters(value):
    '''check if string has  special characters or numbers
    '''
    if not re.match(r"[A-Za-z]", value):
        raise ValueError("contains special characters or numbers")


def valid_location(value):
    '''check if the location is valid
    '''
    if not re.match(r'^[0-9]{1,2}[NS],[0-9]{1,2}[EW]$', value):
        raise ValueError(" ensure you location formatted as a "
                         "latitude-longitude coordinate e.g '12N,67E'")


# implement validation using reqparse


PARSER = reqparse.RequestParser(bundle_errors=True)
PARSER.add_argument('type',
                    type=str,
                    required=True,
                    choices=("Redflag", "Intervention"),
                    help="type field cannot be left "
                         "blank or Bad choice: {error_msg},400"
                    )

PARSER.add_argument('location',
                    type=valid_location,
                    required=True,
                    help="location field cannt be left blank or"
                    " {error_msg},400"
                    )
PARSER.add_argument('images',
                    action='append',
                    help="images field can be left blank!"
                    )
PARSER.add_argument('videos',
                    action='append',
                    help="videos field can be left blank!"
                    )

PARSER.add_argument('comment',
                    type=valid_characters,
                    required=True,
                    help="comment field cannt be left blank or {error_msg},400"
                    )


class Interventions(Resource):
    """intevention class with get and post methods"""
    @jwt_required
    def get(self):
        """get method: gets all interventions for the current user """
        current_user = get_jwt_identity()
        identity = DB.check_current_user_all_incidents(current_user)
        if identity:
            interventions = DB.get_all_interventions_records(current_user)
            return make_response(jsonify({
                "status": 200,
                "data": interventions
            }), 200)
        return{"message": "you dont have any Incidents yet."}

    @jwt_required
    def post(self):
        """post method:posts interventions for the current user"""
        PARSER.parse_args()
        data = request.get_json(silent=True)
        current_user = get_jwt_identity()
        posted = (data['type'], data['location'],
                  data['Images'], data['Videos'], data['comment'],
                  current_user)
        DB.create_intervention_record(posted)
        recent_id = DB.fetch_recent_id()
        return{"status": 201, "data": [{"id": recent_id[0],
                                        "message":"Created intervention record"}]}, 201


class Intervention(Resource):
    """contains the get and delete by id methods """
    @jwt_required
    def get(self, intervention_id):
        """get method:fetchs the record of current user by id"""
        intervention = DB.findOne(intervention_id)
        current_user = get_jwt_identity()
        if intervention:
            check_user = (intervention_id, current_user)
            identity = DB.check_current_user(check_user)
            if identity:
                intervention_s = DB.get_specific_intervention_record(
                    intervention_id)
                return make_response(jsonify({
                    "status": 200,
                    "data": intervention_s
                }), 200)
            return{"message": "Incident id not associated with current account."}
        return {"status": 404,
                "data": [{
                    "message": "intervention record does not exist."
                }]}, 404

    @jwt_required
    def delete(self, intervention_id):
        """delete method:deletes the record by id of the current user"""
        intervention = DB.findOne(intervention_id)
        current_user = get_jwt_identity()
        if intervention:
            check_user = (intervention_id, current_user)
            identity = DB.check_current_user(check_user)
            if identity:
                DB.delete_specific_record(intervention_id)
                return make_response(jsonify({
                    "status": 200,
                    "data": [{"id": intervention_id,
                              "message": "Intervention record has been deleted"}]
                }), 200)
            return{"message": "Incident id not associated with current account."}
        return {"status": 404,
                "data": [{
                    "message": "intervention record does not exist."
                }]}, 404


class Updatecomment(Resource):
    """contains the patch by id method."""
    @jwt_required
    def patch(self, intervention_id):
        """pathch method:patch by id  the comment field of the current user"""
        patch_comment = reqparse.RequestParser(bundle_errors=True)
        patch_comment.add_argument('comment',
                                   type=valid_characters,
                                   required=True,
                                   help="comment field cannt be left blank or"
                                   "{error_msg},400"
                                   )

        patch_comment.parse_args()
        data = request.get_json(silent=True)
        comment = data["comment"]
        patched = (comment, intervention_id)
        intervention = DB.findOne(intervention_id)
        current_user = get_jwt_identity()
        if intervention:
            check_user = (intervention_id, current_user)
            identity = DB.check_current_user(check_user)
            if identity:
                DB.update_intervention_comment(patched)
                return{"status": 200, "data":
                       [{"id": intervention_id, "message":
                         "Updated intervention's comment"}]}, 200
            return{"message": "Incident id not associated with current account."}
        return {"status": 404,
                "data": [{
                    "message": "intervention record does not exist."
                }]}, 404


class Updatelocation(Resource):
    """patch method for the location"""
    @jwt_required
    def patch(self, intervention_id):
        """patch method:patch the location of the current user"""
        patch_location = reqparse.RequestParser(bundle_errors=True)
        patch_location.add_argument('location',
                                    type=valid_location,
                                    required=True,
                                    help="location field cannt be left blank or"
                                    "{error_msg},400"
                                    )

        patch_location.parse_args()
        data = request.get_json(silent=True)
        location = data["location"]
        patched = (location, intervention_id)
        intervention = DB.findOne(intervention_id)
        current_user = get_jwt_identity()
        if intervention:
            check_user = (intervention_id, current_user)
            identity = DB.check_current_user(check_user)
            if identity:
                DB.update_intervention_location(patched)
                return{"status": 200, "data":
                       [{"id": intervention_id, "message":
                         "Updated intervention's location"}]}, 200
            return{"message": "Incident id not associated with current account."}
        return {"status": 404,
                "data": [{
                    "message": "intervention record does not exist."
                }]}, 404


class AdminUpdatesInterventiontatus(Resource):
    """patch method for intervention types"""
    @jwt_required
    def patch(self, intervention_id):
        """only the Admin can patch the intervention type and change the 
            status
        """
        patch_inter_status = reqparse.RequestParser(bundle_errors=True)
        patch_inter_status.add_argument('type',
                                        type=str,
                                        required=True,
                                        choices=("Intervention"),
                                        help="type field cannot be left "
                                        "blank or Bad choice: {error_msg},400"
                                        )
        patch_inter_status.add_argument('status',
                                        type=str,
                                        required=True,
                                        choices=("under investigation",
                                                 "rejected", "resolved"),
                                        help="status field cannot be left "
                                        "blank or Bad choice: {error_msg},400"
                                        )

        data = patch_inter_status.parse_args()
        current_user = get_jwt_identity()
        valid = DB.check_isadmin(current_user)
        if valid is False:
            return {"status": 403, "message": "Only Admin User Has "
                    "access this route."}, 403
        status = data["status"]
        patched = (status, intervention_id)
        intervention = DB.findOne(intervention_id)
        if intervention:
            DB.update_intervention_status(patched)
            return{"status": 200, "data":
                   [{"id": intervention_id, "message":
                     "Updated intervention record status"}]}, 200
        return {"status": 404,
                "data": [{
                    "message": "intervention record does not exist."
                }]}, 404


class AdminupdateRedflagstatus(Resource):
    """patch method for the redflag type"""
    @jwt_required
    def patch(self, intervention_id):
        """Admin user can change the redflag type status"""
        patch_redflag = reqparse.RequestParser(bundle_errors=True)
        patch_redflag.add_argument('type',
                                   type=str,
                                   required=True,
                                   choices=("Redflag"),
                                   help="type field cannot be left "
                                   "blank or Bad choice: {error_msg},400"
                                   )
        patch_redflag.add_argument('status',
                                   type=str,
                                   required=True,
                                   choices=("under investigation",
                                            "rejected", "resolved"),
                                   help="status field cannot be left "
                                   "blank or Bad choice: {error_msg},400"
                                   )

        data = patch_redflag.parse_args()
        current_user = get_jwt_identity()
        valid = DB.check_isadmin(current_user)
        if valid is False:
            return {"status": 403, "message": "Only Admin User Has "
                    " access this route."}, 403
        status = data["status"]
        patched = (status, intervention_id)
        intervention = DB.findOne(intervention_id)
        if intervention:
            DB.update_redflag_status(patched)
            return{"status": 200, "data":
                   [{"id": intervention_id, "message":
                     "Updated redflag record status"}]}, 200
        return {"status": 404,
                "data": [{
                    "message": "intervention record does not exist."
                }]}, 404
