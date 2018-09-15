from werkzeug.security import safe_str_cmp  # per comparare stringhe ed evitare cazzi con gli encoding
from models.user import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)  # prima usavamo i dizionari con username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)  # prima usavamo i dizionari con userid_mapping.get(user_id, None)
