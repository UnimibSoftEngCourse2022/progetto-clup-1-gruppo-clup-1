from app import app, csrf
from flask import render_template, url_for, redirect
from providers.basic_store_provider import BasicStoreProvider
from usecases.book_usecase import BookUseCase
from usecases.consume_reservation_usecase import ConsumeReservationUseCase

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


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


@app.route('/<string:store_id>')
def store_page(store_id):
    queue = bsp.get_queue(store_id)

    return render_template('store_page.html', store=store_id, queue=queue)


@app.route('/<string:store_id>/consume', methods = ['GET', 'POST'])
def consume_page(store_id):
    form = ConsumeForm()
    if form.validate_on_submit():
        b = ConsumeReservationUseCase(bsp)
        res = (form.reservation_id.data.strip(), store_id)
        b.execute(res)
        queue = bsp.get_queue(store_id)
        return redirect(url_for('store_page', store_id=store_id, queue=queue, form=form))
    return render_template('consume.html', form=form, store_id=store_id)


@app.route('/reservation/<string:store_id>')
def reservation(store_id):
    new_res = BookUseCase(bsp)
    new_res.execute(store_id)
    queue = bsp.get_queue(store_id)
    return redirect(url_for('store_page', store_id=store_id, queue=queue))

