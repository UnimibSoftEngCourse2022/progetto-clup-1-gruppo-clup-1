from flask import render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from src.clup.app import app, csrf
from src.clup.providers.basic_store_provider import BasicStoreProvider
from src.clup.usecases.book_usecase import BookUseCase
from src.clup.usecases.consume_reservation_usecase import ConsumeReservationUseCase


class ConsumeForm(FlaskForm):
    reservation_id = StringField(label='reservation')
    submit = SubmitField(label='usa prenotazione')


bsp = BasicStoreProvider()
bsp.add_store('Esselunga')
bsp.add_store('Tigros')
b = BookUseCase(bsp)
b.execute('Esselunga')
b.execute('Esselunga')
b.execute('Tigros')
b.execute('Tigros')



@app.route('/')
def home():
    return render_template('home.html', bsp=bsp)


@app.route('/<string:store_id>', methods=['GET', 'POST'])
def store_page(store_id):
    queue = bsp.get_queue(store_id)
    form = ConsumeForm()
    if form.validate_on_submit():
        b = ConsumeReservationUseCase(bsp)
        res = (form.reservation_id.data, store_id)
        val = b.execute(res)
        print(val)
        print(res[0], res[1])
        return redirect(url_for('store_page', store_id=store_id, queue=queue, form=ConsumeForm()))
    return render_template('store_page.html', store=store_id, queue=queue, form=form)


@app.route('/reservation/<string:store_id>')
def reservation(store_id):
    new_res = BookUseCase(bsp)
    new_res.execute(store_id)
    queue = bsp.get_queue(store_id)
    return redirect(url_for('store_page', store_id=store_id, queue=queue, form=ConsumeForm()))

