from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ChangePasswordForm(FlaskForm):
    old_password = StringField(label='Old password', validators=[DataRequired()])
    new_password = StringField(label='New password', validators=[DataRequired()])
    submit = SubmitField(label='login')
