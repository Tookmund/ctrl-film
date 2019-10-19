from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField

class upload(FlaskForm):
    url = StringField("URL")
    f = FileField("Video File")
    submit = SubmitField("Submit")
