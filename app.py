from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # il file è al root folder del progetto
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # per sapere quando una cosa è cambiata ma non salvata, spegniamo quello di flask dato che c'è quella di sqlalchemy già
app.secret_key = 'jose'  # la secret key per la crittazione del JWT
api = Api(app)  # assegna i verbi alle risorse

jwt = JWT(app, authenticate, identity)  # prende l'app e le funzioni, crea un endpoint /auth e manda username/password alla funzione di autenticazione

api.add_resource(Store, '/store/<string:name>')
# qua settiamo gli endpoint e nella classe impostiamo i verbi permessi
# implementandoli come metodi (che danno un dict e lo status)
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db  # importiamo qua per evitare circular import
    db.init_app(app)
    app.run(port=5000, debug=True)
