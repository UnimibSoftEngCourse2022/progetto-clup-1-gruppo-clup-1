from flask_wtf import FlaskForm
from wtforms import SubmitField


class RegistrationForm(FlaskForm):
    user_register = SubmitField(label='user_registration')
    admin_register = SubmitField(label='admin_register')
    store_manager_register = SubmitField(label='store_manager_register')
