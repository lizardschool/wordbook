from flask_wtf import Form
from wtforms import StringField
from wtforms import validators


class CardlistForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=35), validators.DataRequired()])
