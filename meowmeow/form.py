from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms.fields import SubmitField, TextAreaField

class addPost(FlaskForm):
    title = TextAreaField("let's friend know what's on your mind...")
    img = FileField('img link')

    button = SubmitField('Post')