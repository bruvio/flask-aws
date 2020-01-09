from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.store import StoreModel
from db import db


class Store(Resource):
    @jwt_required()  # d() # we have to authenticate before we run the get method
    def get(self, name):
        try:
            store = StoreModel.find_by_name(name)
        except:
            return (
                {"message": "an Error has occurred inserting the item"},
                500,
            )  # internal server error
        if store:
            return store.json()
        return {"message": "Store not found"}, 404

    @jwt_required()  # we have to authenticate before we run the get method
    def post(self, name):
        # error first approach
        if StoreModel.find_by_name(name):
            return (
                {"message": "an store with name '{}' already exists".format(name)},
                400,
            )  # bad request
        # once error are cleared we deal with what we want to do

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "an Error has occurred inserting the item"}, 500

        return store.json(), 201

    # to implement authentication another package is needed Flask-JWT
    @jwt_required()  # we have to authenticate before we run the get method
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"message": "store deleted"}, 200
        return {"message": "store not found."}, 404


class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}, 200
