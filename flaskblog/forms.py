from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
from flaskblog import bcrypt


class RegistrationForm(FlaskForm):
	username = StringField(
		'Username',
		validators=[
			DataRequired(),
			Length(min=2, max=20)
		])
	email = StringField(
		'Email',
		validators=[
			DataRequired(),
			Email()
		])
	password = PasswordField(
		'Password',
		validators=[
			DataRequired()
		])
	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(
			username=username.data
		).first()
		if user:
			raise ValidationError('username taken dumbass!!')

	def validate_email(self, email):
		user = User.query.filter_by(
			email=email.data
		).first()
		if user:
			raise ValidationError('email taken dumbass!!')


class LoginForm(FlaskForm):
	email = StringField(
		'Email',
		validators=[
			DataRequired(),
			Email()
		])
	password = PasswordField(
		'Password',
		validators=[DataRequired()]
	)
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


class UpdateUser(FlaskForm):
	username = StringField(
		'Username',
		validators=[
			DataRequired(),
			Length(min=2, max=20)
		])
	email = StringField(
		'Email',
		validators=[
			DataRequired(),
			Email()
		])
	description = TextAreaField(
		'Content',
		validators=[
			DataRequired(),
			Length(max=500)
		])
	picture = FileField(
		'Update Profile Picture',
		validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])]
	)
	submit = SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(
				username=username.data
			).first()
			if user:
					raise ValidationError('username taken dumbass!!')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(
				email=email.data
			).first()
			if user:
				raise ValidationError('email taken dumbass!!')


class CreatePost(FlaskForm):
	title = StringField(
		'Title',
		validators=[
			DataRequired(),
			Length(min=1, max=50)
		])
	content = TextAreaField(
		'Content',
		validators=[
			DataRequired(),
			Length(min=1, max=500)
		])
	submit = SubmitField('Create')


class CreateComment(FlaskForm):
	content = TextAreaField(
		'Comment',
		validators=[
			DataRequired(),
			Length(min=1, max=500)
		])
	submit = SubmitField('Send')
