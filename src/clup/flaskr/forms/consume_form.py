from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class ConsumeForm(FlaskForm):
    reservation_id = StringField(label='reservation')
    submit = SubmitField(label='usa prenotazione')