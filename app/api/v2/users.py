"""contains the signup,login,users,AdminIncidents classes"""
from datetime import timedelta
from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from werkzeug.security import generate_password_hash
from flask_jwt_extended import(
    jwt_required, create_access_token, get_jwt_identity)
from .models import Model


EXPIRES = timedelta(minutes=60)
DB = Model()
DB.create_tables()


class Signup(Resource):
    """sign up class contains the post method for registration"""

    def post(self):
        """post method to sign up new users"""
        parser_signup = reqparse.RequestParser(bundle_errors=True)

        parser_signup.add_argument("username",
                                   type=str,
                                   required=True,
                                   help="Username field is required.")
        parser_signup.add_argument("password",
                                   type=str,
                                   required=True,
                                   help="Password field is required .")
        parser_signup.add_argument("email",
                                   type=str,
                                   required=True,
                                   help="Email field is required .")
        parser_signup.add_argument("firstname",
                                   type=str,
                                   help="Firstname field is optional.")
        parser_signup.add_argument("lastname",
                                   type=str,
                                   help="Lastname field is optional .")
        parser_signup.add_argument("phoneNumber",
                                   type=int,
                                   help="Phone number field is optional.")
        parser_signup.add_argument("othername",
                                   type=str,
                                   help="othername field is optional.")

        data = parser_signup.parse_args()
        is_admin = False
        username, password = data["username"], data["password"]
        pw_hash = generate_password_hash(password)
        email = data["email"]
        firstname = data["firstname"]
        lastname = data["lastname"]
        valid_data = DB.validate_user_details(username, email)
        if valid_data:
            user = DB.list_users()
            if user is None:
                is_admin = True
            access_token = create_access_token(
                identity=username, expires_delta=EXPIRES)
            posted = (firstname,  lastname,
                      data['othername'], email, data['phoneNumber'],
                      username, pw_hash, is_admin)
            DB.save_user_details(posted)
            return{"status": 201, "data":
                   [{"token": access_token, "user": data}]}, 201
        return {"status": 400, "message": "check your sign up credentials .Signup failed"}, 400


class Login(Resource):
    """class to login users"""

    def post(self):
        """post method tho allow signed up users to login"""
        parser_login = reqparse.RequestParser(bundle_errors=True)

        parser_login.add_argument("username",
                                  type=str,
                                  required=True,
                                  help="Username field is required.")
        parser_login.add_argument("password",
                                  type=str,
                                  required=True,
                                  help="Password field is required.")
        data = parser_login.parse_args()
        username, password = data["username"], data["password"]
        valid_login = DB.login_user(username, password)
        if valid_login:
            access_token = create_access_token(
                identity=username, expires_delta=EXPIRES)
            return{"status": 200, "data":
                   [{"token": access_token, "user": data}]}, 200
        return {"status": 400, "message": "Bad credentials.Login failed"}, 400


class Users(Resource):
    """class which allows Admin user to see all signedup users"""
    @jwt_required
    def get(self):
        """get method to fetch all signed up users"""
        current_user = get_jwt_identity()
        valid = DB.check_isadmin(current_user)
        if valid is False:
            return {"status": 403, "message": "Only Admin User Has "
                    " access this route."}, 403
        users = DB.get_all_users()
        return make_response(jsonify({
            "status": 200,
            "data": users
        }), 200)


class AdminIncidents(Resource):
    """class which allows admin user to fetch all incidents posted by users"""
    @jwt_required
    def get(self):
        """get method the fetch all incidents.only admin user is allowed to this route """
        current_user = get_jwt_identity()
        valid_user = DB.check_isadmin(current_user)
        if valid_user is False:
            return {"status": 403, "message": "Only Admin User Has "
                    " access this route."}, 403
        users = DB.get_all_incindents()
        return make_response(jsonify({
            "status": 200,
            "data": users
        }), 200)
