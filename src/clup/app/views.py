import flask_login
from app import app, csrf, login_manager
from flask import render_template, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user
from flask_wtf.csrf import CSRFError
from providers.basic_store_provider import BasicStoreProvider
from usecases.book_usecase import BookUseCase
from usecases.consume_reservation_usecase import ConsumeReservationUseCase

from .flask_user import FlaskUser
from .forms.change_password import ChangePasswordForm
from .forms.consume_form import ConsumeForm
from .forms.user_login_form import UserLoginForm
from .forms.user_register_form import UserRegisterForm
from src.clup.entities.user import User
from src.clup.providers.basic_user_provider import BasicUserProvider
from src.clup.usecases.user_register_usecase import UserRegisterUsecase
from src.clup.usecases.user_login_usecase import UserLoginUseCase
from src.clup.usecases.user_change_password_usecase import UserChangePasswordUseCase
from src.clup.usecases.load_user_data_usecase import LoadUserDataUseCase

bsp = BasicStoreProvider()
bsp.add_store('Esselunga')
bsp.add_store('Tigros')
b = BookUseCase(bsp)
b.execute('Esselunga')
b.execute('Esselunga')
b.execute('Tigros')
b.execute('Tigros')

bup = BasicUserProvider()
ur_def = UserRegisterUsecase(bup)
ur_def.execute('davide', 'prova')


@login_manager.user_loader
def load_user(u_id):
    users = bup.get_users()
    if u_id in [user.id for user in users]:
        return FlaskUser(u_id)
    else:
        return None


@app.route('/')
def home():
    return render_template('home.html', bsp=bsp)


@app.route('/<string:store_id>')
def store_page(store_id):
    queue = bsp.get_queue(store_id)

    return render_template('store_page.html', store=store_id, queue=queue)


@app.route('/<string:store_id>/consume', methods=['GET', 'POST'])
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
        username = form.username.data
        password = form.password1.data
        ur = UserRegisterUsecase(bup)
        try:
            ur.execute(username, password)
            return redirect(url_for('user_login_page'))
        except ValueError:
            flash('Something went wrong', category='danger')
            return redirect(url_for('user_register_page'))
    elif form.is_submitted():
        flash("check all fields", category='danger')
    return render_template('user_register.html', form=form)


@app.route('/registered_users')
def show_registered_users():
    return render_template('registered_users.html', users=bup.get_users())


@app.route('/user/login', methods=['GET', 'POST'])
def user_login_page():
    form = UserLoginForm()
    if form.validate_on_submit():
        ul = UserLoginUseCase(bup)
        username = form.username.data
        password = form.password.data
        try:
            u_id = ul.execute(username, password)
            user = FlaskUser(u_id)
            login_user(user)
            return redirect(url_for('user_page'))
        except ValueError:
            flash('Something went wrong', category='danger')
            return redirect(url_for('user_login_page'))
    else:
        if form.is_submitted():
            flash('form not valid', category='danger')
    return render_template('user_login.html', form=form)


@app.route('/user/account')
@login_required
def user_page():
    u_id = flask_login.current_user.get_id()
    user_data = LoadUserDataUseCase(bup).execute(u_id)
    return render_template('user.html', user=user_data)


@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("you must login first", category='danger')
    return redirect(url_for('user_login_page'))


@app.route('/logout')
def user_logout():
    logout_user()
    return redirect(url_for('user_login_page'))


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400


@app.route('/user/account/change_password', methods=['GET', 'POST'])
@login_required
def change_password_page():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        old_password = form.old_password.data
        new_password = form.new_password.data
        ucp = UserChangePasswordUseCase(bup)
        try:
            username = LoadUserDataUseCase(bup).execute(flask_login.current_user.get_id()).username
            ucp.execute(username, old_password, new_password)
            return redirect(url_for('user_logout'))
        except ValueError:
            flash('Something went wrong', category='danger')
            return redirect(url_for('change_password_page'))
    else:
        if form.is_submitted():
            flash('form not valid', category='danger')
    return render_template('change_password.html', form=form)
