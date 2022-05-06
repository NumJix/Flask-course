import sqlite3
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type = float,
        required = True,
        help = 'This field cannot be empty.'
    )
    parser.add_argument(
        'store_id',
        type = float,
        required = True,
        help = 'Every item needs a store ID.'
    )
    
    # @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {name: 'not available'}, 404
        
    def post(self, name):       
        if ItemModel.find_by_name(name):
        #above line can also be if Item.find_by_name(name)
            return {'item': '{} already exists'.format(name)}, 400
        
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])
        # name is obtained from the address bar        
        
        try:
            item.save_to_db()
        except:
            return {'warning': 'An error occured! While inserting the item.'}, 500
            
        return item.json(), 201 #201 code for created, 202 for accepted
    
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()                    
            # ItemModel.delete_from_db(item)
            return {name: "deleted"}
    
        return {name: 'not in store'}
    
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        
        if item is None:
            item = ItemModel(name, **data)
            # the arguments are passed in as Kwargs       
        else:
            item.price = data['price']
            item.store_id = data['store_id']
            # item is a json object. not a dictionary yet. thats why we used item.price
        item.save_to_db()
        return item.json(), 201
    
    
class ItemList(Resource):
    @jwt_required()
    def get(self):
        
        return {
            "items": [item.json() for item in ItemModel.query.all()]
            # items: list(map(lambda x: x.json(), ItemModel.query.all))
        }