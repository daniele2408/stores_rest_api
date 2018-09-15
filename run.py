from app import app
from db import db

db.init_app(app)

@app.before_first_request  # lancia la funzione che crea le tabelle (è tutti già definito nei Model) subito per prima cosa
def create_tables():
    db.create_all()