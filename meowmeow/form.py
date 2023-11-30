from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms.fields import SubmitField, TextAreaField
from wtforms.validators import DataRequired

class addPost(FlaskForm):
    title = TextAreaField("let's friend know what's on your mind...", validators=[DataRequired()])
    img = FileField('', validators=[FileRequired()])

    button = SubmitField('Post')


class editPost(FlaskForm):
    title = TextAreaField("let's friend know what's on your mind...")
    img = FileField('')
    button = SubmitField('Edit')