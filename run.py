#!/bin/python3
from flaskblog import app
from os import listdir

if __name__ == "__main__":
	if 'db.sqlite3' not in listdir():
		from flaskblog import db
		app.app_context().push()
		db.create_all()
	app.run(debug=True)
