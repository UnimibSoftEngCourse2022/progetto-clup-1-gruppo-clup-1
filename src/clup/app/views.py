from app import app
from flask import render_template, url_for, redirect
from providers.basic_store_provider import BasicStoreProvider
from usecases.book_usecase import BookUseCase

bsp = BasicStoreProvider()
bsp.add_store('Esselunga')
bsp.add_store('Tigros')
bsp.set_queue('Esselunga', ('cliente1', 'cliente2'))
bsp.set_queue('Tigros', ('cliente3', 'cliente4'))


@app.route('/')
def home():
    return render_template('home.html', bsp=bsp)


@app.route('/<string:store_id>')
def store_page(store_id):
    queue = bsp.get_queue(store_id)
    return render_template('store_page.html', store=store_id, queue=queue)


@app.route('/reservation/<string:store_id>')
def reservation(store_id):
    new_res = BookUseCase(bsp)
    new_res.execute(store_id)
    queue = bsp.get_queue(store_id)
    return redirect(url_for('store_page', store_id=store_id, queue=queue))

