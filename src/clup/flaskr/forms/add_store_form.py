from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddStoreForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    address = StringField(label='Address', validators=[DataRequired()])
    submit = SubmitField(label='Add Store')
