from flaskblog import app
from os import listdir
from time import sleep
from flaskblog.utils import create_db


if __name__ == "__main__":
    if not listdir('instance'):
        create_db()
    app.run(debug=True)
