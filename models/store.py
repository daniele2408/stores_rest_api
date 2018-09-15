from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)  # aggiungiamo id
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')  # riferimento a ItemModel, e lo risolve da sé perché specificato in ItemModel
                                                          # con lazy='dynamic' evitiamo che crei un oggetto ItemModel ogni volta che creiamo uno StoreModel, ma solo quando usiamo il metodo .json()
    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  # equivale a SELECT * FROM items WHERE name=$name LIMIT 1

    def save_to_db(self):
        db.session.add(self)  # session è la collezione di oggetti che aggiungeremo
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
