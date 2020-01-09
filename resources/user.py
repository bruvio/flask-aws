# will define a user object

import sqlite3

from flask_restful import Resource, reqparse
from models.user import UserModel

# so this class can interact with sql lite


class UserRegister(Resource):
    parser = (
        reqparse.RequestParser()
    )  # initialize a new object the initialize the request
    parser.add_argument(
        "username", type=str, required=True, help="name field cannot be left blank"
    )
    parser.add_argument(
        "password", type=str, required=True, help="password field cannot be left blank"
    )

    def post(self):
        data = (
            UserRegister.parser.parse_args()
        )  # is going to parse the argument that come throught the json payload
        if UserModel.find_by_username(
            data["username"]
        ):  # if there is a user with that username we are using tor register
            return {"message": "User already registered "}, 400

        user = UserModel(**data)
        user.save_to_db()
        return {"message": "User created successfully"}, 201  # resource created

        # this is the method that is going to be called when we post resources
