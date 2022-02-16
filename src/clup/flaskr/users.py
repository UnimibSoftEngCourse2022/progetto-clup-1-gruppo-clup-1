from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from src.clup.entities.admin import Admin
from src.clup.flaskr.global_setup import bup, bap, bsp, bqp, brp
from src.clup.usecases.admin_register_usecase import AdminRegisterUsecase
from src.clup.usecases.generic_login_usecase import GenericLoginUsecase
from src.clup.usecases.load_admin_data_usecase import LoadAdminDataUseCase
from src.clup.usecases.load_user_data_usecase import LoadUserDataUseCase
from src.clup.usecases.user_change_password_usecase import UserChangePasswordUseCase
from src.clup.usecases.user_register_usecase import UserRegisterUsecase
from . import stores

from .flask_user import FlaskUser
from .forms.change_password import ChangePasswordForm
from .forms.search_store_form import SearchStoreForm
from .forms.user_login_form import UserLoginForm
from .forms.user_register_form import UserRegisterForm
from .forms.user_reservation_form import UserReservationForm
from src.clup.usecases.make_reservation_usecase import MakeReservationUseCase
from src.clup.usecases.consume_reservation_usecase import ConsumeReservationUseCase

bp = Blueprint('users', __name__)

ur_def = UserRegisterUsecase(bup)
ur_def.execute('davide', 'prova')
ar_def = AdminRegisterUsecase(bap)
ar_def.execute('amministratore', 'password')

mru = MakeReservationUseCase(bqp, brp)
cru = ConsumeReservationUseCase(bqp)


# TO FIX
# @app.route('/')
# def home():
#     return render_template('home.html', bsp=bsp)


@bp.route('/register', methods=['GET', 'POST'])
def user_register_page():
    form = UserRegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password1.data
        ur = UserRegisterUsecase(bup)
        try:
            ur.execute(username, password)
            return redirect(url_for('users.user_login_page'))
        except ValueError:
            flash('Something went wrong', category='danger')
            return redirect(url_for('users.user_register_page'))
    elif form.is_submitted():
        flash("check all fields", category='danger')
    return render_template('user_register.html', form=form)


# @app.route('/registered_users')
# def show_registered_users():
#     return render_template('registered_users.html', users=bup.get_users())


@bp.route('/login', methods=['GET', 'POST'])
def user_login_page():
    print(bup.get_users())
    print(bap.get_admins())
    form = UserLoginForm()
    if form.validate_on_submit():
        gl = GenericLoginUsecase(bap, bup)
        username = form.username.data
        password = form.password.data
        try:
            u_id, logged_type = gl.execute(username, password)
            user = FlaskUser(u_id)
            login_user(user)
            if logged_type == 'user':
                return redirect(url_for('users.user_page'))
            if logged_type == 'admin':
                return redirect(url_for('stores.show_stores'))
        except ValueError:
            flash('Incorrent credentials', category='danger')
            return redirect(url_for('users.user_login_page'))
    else:
        if form.is_submitted():
            flash('form not valid', category='danger')
    return render_template('user_login.html', form=form)


@bp.route('/account', methods=['GET', 'POST'])
@login_required
def user_page():
    u_id = current_user.get_id()
    user_data = LoadUserDataUseCase(bup).execute(u_id)
    form = SearchStoreForm()
    st = bsp.get_stores()
    if form.validate_on_submit():
        store_list = stores.search_store(form.store.data)
        print(store_list)
        return redirect(url_for('users.founded_store', stores=store_list))

    return render_template('user.html', user=user_data, form=form, st=st)


@bp.route('/founded_store/<stores>')
def founded_store(stores):
    u_id = current_user.get_id()
    user_data = LoadUserDataUseCase(bup).execute(u_id)
    return render_template('founded_store.html', stores=stores, user=user_data)


@bp.route('/reservation/<store_id>', methods=['GET', 'POST'])
def user_reservation(store_id):
    u_id = current_user.get_id()
    user_data = LoadUserDataUseCase(bup).execute(u_id)
    form = UserReservationForm()

    if form.validate_on_submit():
        reservation = mru.execute(store_id, u_id)
        return redirect(url_for('users.user_make_reservation', store_id=store_id, user=user_data, form=form,
                                reservation_id=reservation.id))

    return render_template('user_reservation.html', store=store_id, user=user_data, form=form)


@bp.route('/reservation/<store_id>/<reservation_id>', methods=['GET', 'POST'])
def user_make_reservation(store_id, reservation_id):
    u_id = current_user.get_id()
    user_data = LoadUserDataUseCase(bup).execute(u_id)
    form = UserReservationForm()
    return render_template('user_reservation.html', store=store_id, user=user_data, form=form, reservation_id=reservation_id)


@bp.route('/admin/account')
@login_required
def admin_page():
    a_id = current_user.get_id()
    admin_data = LoadAdminDataUseCase(bap).execute(a_id)
    return render_template('admin.html', admin=admin_data)


@bp.route('/logout')
def user_logout():
    logout_user()
    return redirect(url_for('users.user_login_page'))


# TODO
# @app.errorhandler(CSRFError)
# def handle_csrf_error(e):
#     return render_template('csrf_error.html', reason=e.description), 400


@bp.route('/account/change_password', methods=['GET', 'POST'])
@login_required
def change_password_page():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        old_password = form.old_password.data
        new_password = form.new_password.data
        ucp = UserChangePasswordUseCase(bup)
        try:
            username = LoadUserDataUseCase(bup).execute(current_user.get_id()).username
            ucp.execute(username, old_password, new_password)
            return redirect(url_for('users.user_logout'))
        except ValueError:
            flash('Something went wrong', category='danger')
            return redirect(url_for('users.change_password_page'))
    else:
        if form.is_submitted():
            flash('form not valid', category='danger')
    return render_template('change_password.html', form=form)
