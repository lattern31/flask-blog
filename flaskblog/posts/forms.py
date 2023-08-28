from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

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
        'Content',
		validators=[
			DataRequired(),
			Length(min=1, max=500)
		])
	submit = SubmitField('Send')

