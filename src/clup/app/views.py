from app import app, csrf
from flask import render_template, url_for, redirect
from providers.basic_store_provider import BasicStoreProvider
from usecases.book_usecase import BookUseCase
from usecases.consume_reservation_usecase import ConsumeReservationUseCase


from .forms.consume_form import ConsumeForm
from .forms.user_register_form import UserRegisterForm
from src.clup.entities.user import User
from src.clup.providers.basic_user_provider import BasicUserProvider
from src.clup.usecases.user_register_usecase import UserRegisterUsecase

bsp = BasicStoreProvider()
bsp.add_store('Esselunga')
bsp.add_store('Tigros')
b = BookUseCase(bsp)
b.execute('Esselunga')
b.execute('Esselunga')
b.execute('Tigros')
b.execute('Tigros')

bup = BasicUserProvider()



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


@app.route('/user/register', methods=['GET', 'POST'])
def user_register_page():
    form = UserRegisterForm()
    if form.validate_on_submit():
        new_user = User(id=form.user_id.data, password=form.password1.data)
        ur = UserRegisterUsecase(bup)
        ur.execute(new_user)
        return redirect(url_for('show_registered_users'))#TODO
    return render_template('user_register.html', form=form)


@app.route('/registered_users')
def show_registered_users():
    return render_template('registered_users.html', users=bup.get_users())