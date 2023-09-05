from flaskblog import db, login_manager, bcrypt
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import desc


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

post_likes = db.Table(
					'post_likes',
					db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
					db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
					)

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100), unique=True, nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	password_hash = db.Column(db.String(128), nullable=False)

	@property
	def password(self):
		raise AttributeError('password not readable')

	@password.setter
	def password(self, password):
		self.password_hash = bcrypt.generate_password_hash(password)

	def verify_pw(self, pw):
		return bcrypt.check_password_hash(self.password_hash, pw)

	posts = db.relationship('Post', backref="author", lazy=True)
	comments = db.relationship('Comment', backref="author", lazy=True)
	avatar = db.Column(db.String(20), nullable=False, default='default.jpg')
	description = db.Column(db.String(500), nullable=False, default="Hi, I'm new here!")
	
	def __repr__(self) -> str:
		return f"User('{self.id}', '{self.username}', '{self.email}')"


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	content = db.Column(db.String(500), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'),  nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	likes = db.relationship('User', secondary=post_likes, backref='likes')
	comments = db.relationship('Comment', backref="post", lazy=True)
	
	def __repr__(self) -> str:
		return f"Post('{self.id}', '{self.title}', '{self.user_id}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),  nullable=False)
    content = db.Column(db.String(500), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Comment({self.id}, post_id: {self.post_id}, user_id: {self.user_id}, '{self.content}')"

