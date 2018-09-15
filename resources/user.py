import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
        parser = reqparse.RequestParser()  # requisiti per il request
        parser.add_argument('username',
            type=str,
            required=True,
            help="This field cannot be left blank"
        )
        parser.add_argument('password',
            type=str,
            required=True,
            help="This field cannot be left blank"
        )

        def post(self):
            data = UserRegister.parser.parse_args()

            # evitare duplicati nello username
            if UserModel.find_by_username(data['username']):
                return {"message": "A user with that username already exists"}, 400

            user = UserModel(**data)  # con **data non dobbiamo fare altro, prende username e password che gli serve e basta, perché col parser dalla riga 7 sappiamo che avrà sempre e solo quei valori
            user.save_to_db()

            return {"message": "User created successfully."}, 201  # 201 mean created
