from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchStoreForm(FlaskForm):
    store = StringField(label='store_name', validators=[DataRequired()])
    submit = SubmitField(label='search')
