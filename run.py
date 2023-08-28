#!/bin/python3
from flaskblog import app
from os import listdir
from time import sleep


if __name__ == "__main__":
	if 'instance' not in listdir():
		print('creating db')
		from flaskblog import db
		app.app_context().push()
		db.create_all()
	app.run(debug=True)
