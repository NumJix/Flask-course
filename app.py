from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import StoreList, Store

from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
# the above line only turns off the flask-sqlalchemy modifications tracker not the actual sqlalchemy modifications tracker
# sqlalchemy modification tracker is slightly better
app.secret_key = 'Jeryn'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity) #/auth
    
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/itemlist')
api.add_resource(UserRegister, '/register')
api.add_resource(StoreList, '/stores')
api.add_resource(Store, '/store/<string:name>' )

if __name__ == '__main__':
    db.init_app(app)
    #new line need more research
    app.run(debug= True)