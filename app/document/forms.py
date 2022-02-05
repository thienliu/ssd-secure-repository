from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField

class UploadForm(FlaskForm):
    file = FileField('Select a file to upload', validators=[FileRequired()])
    submit = SubmitField('Submit')