from flask import request
from flask_restx import Namespace, Resource

from .service import AuthService
from .model import user_account_model
from application.utilities.jw_token import encode_auth_token
from application.utilities.wrap_functions import admin_token_required


api = Namespace("Auth", description="Authentication related operations")

userAccount = api.model("UserAccount", user_account_model)


@api.route("/admin/register")
class RegisterAdmin(Resource):
    @api.doc(responses={200: 'OK', 201: 'Created', 405: 'Method Not Allowed'})
    @api.expect(userAccount, validate=True)
    @admin_token_required
    def post(self):
        """Create an admin account
        Use this method to create an admin account.
        * Send a JSON object with the detail in the request body.
        ```
        {
          "username": "Username",
          "password": "Password",
        }
        ```
        """
        new_admin = request.json
        admin = AuthService.getAdmin(new_admin["username"])
        if not admin:
            result = AuthService.createAdmin(new_admin["username"], new_admin["password"])
            return result, 201
        else:
            return {"message": "Unable to create because the account with this username already exists"}, 405


@api.route("/admin/login")
class LoginAdmin(Resource):
    @api.doc(responses={200: 'OK', 404: 'Not Found'})
    @api.expect(userAccount, validate=True)
    def post(self):
        """Login as admin account
        Use this method to login with admin rights.
        * Send a JSON object with the detail in the request body.
        ```
        {
          "username": "Username",
          "password": "Password",
        }
        ```
        """
        admin_account = request.json
        admin = AuthService.checkAdminAccount(admin_account["username"], admin_account["password"])
        if not admin:
            return {"message": "Username or password does not match"}, 404
        else:
            token = encode_auth_token(username=admin_account["username"], isAdmin=True)
            result = admin
            result[0]['token'] = token.decode('utf8')
            return result, 200



@api.route("/user/register")
class RegisterUser(Resource):
    @api.doc(responses={200: 'OK', 201: 'Created', 405: 'Method Not Allowed'})
    @api.expect(userAccount, validate=True)
    def post(self):
        """Create an user account
        Use this method to create a user account.
        * Send a JSON object with the detail in the request body.
        ```
        {
          "username": "Username",
          "password": "Password",
        }
        ```
        """
        new_user = request.json
        user = AuthService.getUser(new_user["username"])
        if not user:
            result = AuthService.createUser(new_user["username"], new_user["password"])
            return result, 201
        else:
            return {"message": "Unable to create because the account with this username already exists"}, 405

@api.route("/user/login")
class LoginUser(Resource):
    @api.doc(responses={200: 'OK', 404: 'Not Found'})
    @api.expect(userAccount, validate=True)
    def post(self):
        """Login as user account
        Use this method to login with user rights.
        * Send a JSON object with the detail in the request body.
        ```
        {
          "username": "Username",
          "password": "Password",
        }
        ```
        """
        user_account = request.json
        user = AuthService.checkUserAccount(user_account["username"], user_account["password"])
        if not user:
            return {"message": "Username or password does not match"}, 404
        else:
            token = encode_auth_token(username=user_account["username"], isAdmin=False)
            result = user
            result[0]['token'] = token.decode('utf8')
            return result, 200