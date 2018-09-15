from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()  # requisiti per il request
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank"
    )

    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id"
    )

    @jwt_required()  # per fare get serve autenticarsi
    def get(self, name):  # prende item dalla lista se esiste
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

        # # codice con liste
        # item = next(filter(lambda x: x["name"] == name, items), None)  # primo item dato dalla filter, e se non trova dà un None
        # return {"item": item}, 200 if item else 404  # Status code found / not found

    def post(self, name):  # il post deve avere stessi param di get
        if ItemModel.find_by_name(name):
            return {'message': 'An item with name {} already exists'.format(name)}, 400  # Bad Request nel caso

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'], data['store_id'])  # anche se potremmo mettere solo **data

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500  # internal server error

        return item.json(), 201  # status created

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}


    def put(self, name):
        data = Item.parser.parse_args()  # altrimenti senza requeste parse useremmo request.get_json()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}  # .all() ritorna tutti gli oggetti
