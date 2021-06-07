from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = ' '
api = Api(app)

# JWT creates a new endpoint /auth
# when calling /auth we send it a username and password and the JWT extension sends it to authenticate function
jwt = JWT(app, authenticate, identity)

# This will contain a list of dictionaries
items = []


class Item(Resource):
    @jwt_required()
    def get(self, name):
        # Filter function takes two parameters - A  filtering function and the list of items to filter
        # Lambda 'x' is the name argument in the method call
        item = next(filter(lambda x: x['name'] == name, items), None)    # next - returns first item found by filter function
        return {'item': item}, 200 if item else 404     # 200 if the item exists. If not 404

    #   for item in items:
    #       if item['name'] == name:
    #           return item
    #   return {'item': None}, 404  # 404 - ITEM NOT FOUND

    def post(self, name):
        # If we found an item matching this name and that item is not None that means it is an item
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': f'An item with name {name} already exists.'}, 400



        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201  # So that the application knows this has happened - 201 - CREATED


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')  # http://127.0.0.1:8080/item/<item name>
api.add_resource(ItemList, '/items')
app.run(port=8080, debug=True)
