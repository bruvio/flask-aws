from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel
from db import db


class Item(Resource):
    # @app.route('/item') # three is no need for this!

    parser = (
        reqparse.RequestParser()
    )  # initialize a new object the initialize the request
    parser.add_argument(
        "price", type=float, required=True, help="price field cannot be left blank"
    )
    parser.add_argument(
        "store_id", type=int, required=True, help="Every item need a store id"
    )

    # parser.add_argument(
    #     "name", type=str, required=True, help="name field cannot be left blank"
    # )

    @jwt_required()  # d() # we have to authenticate before we run the get method
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return (
                {"message": "an Error has occurred inserting the item"},
                500,
            )  # internal server error
        if item:
            return item.json()

        return {"message": "Item not found"}, 404

    @jwt_required()  # we have to authenticate before we run the get method
    def post(self, name):
        # error first approach
        if ItemModel.find_by_name(name):
            return (
                {"message": "an item with name '{}' already exists".format(name)},
                400,
            )  # bad request
        # once error are cleared we deal with what we want to do

        data = (
            Item.parser.parse_args()
        )  # is going to parse the argument that come throught the json payload
        # data = request.get_json() # this will fail if we do not set in the header of the request the correct content type and value (json)
        # item = ItemModel(name, data["price"],, data["store_id"])
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {"message": "an Error has occurred inserting the item"}, 500

        return item.json(), 201

    # to implement authentication another package is needed Flask-JWT
    @jwt_required()  # we have to authenticate before we run the get method
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "item deleted"}, 200
        return {"message": "Item not found."}, 404

    @jwt_required()  # we have to authenticate before we run the get method
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            item.price = data["price"]
        else:
            # item = ItemModel(name, data["price"], data["store_id"])
            item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "an Error has occurred inserting the item"}, 500

        return item.json(), 201


class ItemList(Resource):
    TABLE_NAME = "items"

    def get(self):

        return {"items": [item.json() for item in ItemModel.query.all()]}, 200
        # return {"items": list(map(lambda x: x.json(), ItemModel.query.all()))}
