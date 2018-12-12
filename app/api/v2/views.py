import psycopg2
import re
from flask_restful import Resource, reqparse
from flask import jsonify, make_response, request
from .models import Model


db = Model()
db.create_tables()


def is_valid(value):
    '''check if the string is empty'''
    if not value:
        raise ValueError("empty string")


def valid_characters(value):
    '''check if string has  special characters or numbers
    '''
    if not re.match(r"[A-Za-z]", value):
        raise ValueError("contains special characters or numbers")

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
                    type=valid_characters,
                    required=True,
                    help="location field cannt be left blank or {error_msg},400"
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
    def get(self):
        interventions = db.get_all_interventions_records()
        return make_response(jsonify({
            "status": 200,
            "data": interventions
        }), 200)
    
    def post(self):
        PARSER.parse_args()
        data = request.get_json(silent=True)
        posted = (data['id'], data['type'], data['location'],
                  data['Images'], data['Videos'], data['comment'])
        db.create_intervention_record(posted)
        return{"status": 201, "data": [{"id": data['id'],
                                        "message":"Created intervention record"}]}, 201


class Intervention(Resource):
    def get(self, intervention_id):
        intervention = db.get_specific_intervention_record(intervention_id)
        if intervention:
            return make_response(jsonify({
                "status": 200,
                "data": intervention
            }), 200)
        return {"status": 404,
                "data": [{
                    "message": "intervention record does not exist."
                }]}, 404
    
    def delete(self, intervention_id):
        intervention = db.findOne(intervention_id)
        if intervention:
            db.delete_specific_record(intervention_id)
            return make_response(jsonify({
                "status": 200,
                "data": [{"id": intervention_id,
                          "message": "Intervention record has been deleted"}]
            }), 200)
        return {"status": 404,
                "data": [{
                    "message": "intervention record does not exist."
                }]}, 404


class Updatecomment(Resource):
    def patch(self, intervention_id):
        paserrr = reqparse.RequestParser(bundle_errors=True)
        paserrr.add_argument('comment',
                             type=valid_characters,
                             required=True,
                             help="comment field cannt be left blank or"
                             "{error_msg},400"
                             )
        paserrr.parse_args()
        data = request.get_json(silent=True)
        comment = data["comment"]
        patched = (comment, intervention_id)
        intervention = db.findOne(intervention_id)
        if intervention:
            db.update_intervention_comment(patched)
            return{"status": 200, "data":
                   [{"id": intervention_id, "message":
                     "Updated intervention's comment"}]}, 200
        return {"status": 404,
                "data": [{
                    "message": "intervention record does not exist."
                }]}, 404


class Updatelocation(Resource):
    def patch(self, intervention_id):
        paserr = reqparse.RequestParser(bundle_errors=True)
        paserr.add_argument('location',
                            type=valid_characters,
                            required=True,
                            help="location field cannt be left blank or"
                            "{error_msg},400"
                            )
        paserr.parse_args()
        data = request.get_json(silent=True)
        location = data["location"]
        patched = (location, intervention_id)
        intervention = db.findOne(intervention_id)
        if intervention:
            db.update_intervention_location(patched)
            return{"status": 200, "data":
                   [{"id": intervention_id, "message":
                     "Updated intervention's location"}]}, 200
        return {"status": 404,
                "data": [{
                    "message": "intervention record does not exist."
                }]}, 404


class AdminUpdatesInterventiontatus(Resource):
    def patch(self, intervention_id):
        paserr = reqparse.RequestParser(bundle_errors=True)
        paserr.add_argument('type',
                            type=str,
                            required=True,
                            choices=("Intervention"),
                            help="type field cannot be left "
                            "blank or Bad choice: {error_msg},400"
                            )
        paserr.add_argument('isAdmin',
                            type=str,
                            required=True,
                            choices=("True", "False"),
                            help="Only Admin users allowed"
                            " or Bad choice: {error_msg},400"
                            )
        paserr.add_argument('status',
                            type=str,
                            required=True,
                            choices=("under investigation",
                                     "rejected", "resolved"),
                            help="status field cannot be left "
                            "blank or Bad choice: {error_msg},400"
                            )
        paserr.parse_args()
        data = request.get_json(silent=True)
        status = data["status"]
        patched = (status, intervention_id)
        intervention = db.findOne(intervention_id)
        if intervention:
            db.update_intervention_status(patched)
            return{"status": 200, "data":
                   [{"id": intervention_id, "message":
                     "Updated intervention record status"}]}, 200
        return {"status": 404,
                "data": [{
                    "message": "intervention record does not exist."
                }]}, 404


class AdminupdateRedflagstatus(Resource):
    def patch(self, intervention_id):
        paserr = reqparse.RequestParser(bundle_errors=True)
        paserr.add_argument('type',
                            type=str,
                            required=True,
                            choices=("Redflag"),
                            help="type field cannot be left "
                            "blank or Bad choice: {error_msg},400"
                            )
        paserr.add_argument('isAdmin',
                            type=str,
                            required=True,
                            choices=("True", "False"),
                            help="Only Admin users allowed "
                            "or Bad choice: {error_msg},400"
                            )
        paserr.add_argument('status',
                            type=str,
                            required=True,
                            choices=("under investigation",
                                     "rejected", "resolved"),
                            help="status field cannot be left "
                            "blank or Bad choice: {error_msg},400"
                            )
        paserr.parse_args()
        data = request.get_json(silent=True)
        status = data["status"]
        patched = (status, intervention_id)
        intervention = db.findOne(intervention_id)
        if intervention:
            db.update_redflag_status(patched)
            return{"status": 200, "data":
                   [{"id": intervention_id, "message":
                     "Updated redflag record status"}]}, 200
        return {"status": 404,
                "data": [{
                    "message": "intervention record does not exist."
                }]}, 404


class Signup(Resource):
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)

        parser.add_argument("username",
                            type=str,
                            required=True,
                            help="Username field is required.")
        parser.add_argument("password",
                            type=str,
                            required=True,
                            help="Password field is required.")
        parser.add_argument("email",
                            type=str,
                            required=True,
                            help="Email field is required.")
        parser.add_argument("firstname",
                            type=str,
                            help="Firstname field is optional.")
        parser.add_argument("lastname",
                            type=str,
                            help="Lastname field is optional.")
        parser.add_argument("phoneNumber",
                            type=int,
                            help="Phone number field is optional.")

        args = parser.parse_args()
        data = request.get_json(silent=True)
        username = data["username"]
        password = data["password"]
        email = data["email"]
        firstname = data["firstname"]
        lastname = data["lastname"]
        valid_data = db.register_user(username, password, email)
        if valid_data:
            access_token = create_access_token(identity=password)
            posted = (data['firstname'], data['lastname'],
                      data['othername'], email, data['phoneNumber'],
                      username, password)
            db.save_user_details(posted)
            return{"status": 201, "data":
                   [{"token": access_token, "user": data}]}, 201
        return {"message": "Bad credentials.Signup failed"}, 400