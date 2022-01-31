from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import EqualTo


class UserRegisterForm(FlaskForm):
    user_id = StringField(label='User Name')
    password1 = StringField(label='Password')
    password2 = StringField(label='Confirm Password', validators=[EqualTo('password1')])
    submit = SubmitField(label='Register')