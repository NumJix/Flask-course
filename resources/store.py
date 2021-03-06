from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'Message': 'Store not found.'}, 404
    
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'Message': '{} already exists.'.format(name)}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return{'Warning':'Error occured. Please try again.'}, 500
        return store.json(), 201
                
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {name: 'Store deleted.'}
        return {'Message': '{name} doesnot exist'}
            
    
class StoreList(Resource):
    def get(self):
        return {
            'Stores':[store.json() for store in StoreModel.query.all()]
            }