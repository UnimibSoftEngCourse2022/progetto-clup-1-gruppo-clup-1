from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import EqualTo, DataRequired


class StoreManagerRegisterForm(FlaskForm):
    username = StringField(label='User Name', validators=[DataRequired()])
    password1 = StringField(label='Password', validators=[DataRequired()])
    password2 = StringField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    secret_key = StringField(label='Secret Key', validators=[DataRequired()])
    submit = SubmitField(label='Register')
