from flask_wtf import FlaskForm
from wtforms import SubmitField


class UserReservationForm(FlaskForm):

    make_reservation = SubmitField(label='make_reservation')
    delete_reservation = SubmitField(label='delete_reservation')
