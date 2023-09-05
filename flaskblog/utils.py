from flaskblog import app
from os import listdir
from time import sleep


def create_db():
    print('creating db')
    from flaskblog import db
    app.app_context().push()
    db.create_all()

