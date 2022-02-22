from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import EqualTo, DataRequired


class AdminRegisterForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password1 = StringField(label='Password', validators=[DataRequired()])
    password2 = StringField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    store_name = StringField(label='Store Name', validators=[DataRequired()])
    store_address = StringField(label='Store Address', validators=[DataRequired()])
    store_sk = StringField(label='Store SK', validators=[DataRequired()])
    submit = SubmitField(label='Login')