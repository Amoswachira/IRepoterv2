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