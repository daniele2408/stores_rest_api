import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    # definiamo le tre colonne della tabella users, e ce ne devono essere
    # tanti quanti nell'__init__
    id = db.Column(db.Integer, primary_key=True)  # primary key
    username = db.Column(db.String(80))  # max 80 char
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)  # session è la collezione di oggetti che aggiungeremo
        db.session.commit()

    @classmethod  # non si riferisce mai all'istanza ma alla classe
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()  # equivale a SELECT * FROM users WHERE username=$username LIMIT 1

    @classmethod  # non si riferisce mai all'istanza ma alla classe
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
