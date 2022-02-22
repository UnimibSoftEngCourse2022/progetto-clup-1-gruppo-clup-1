from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from .forms.registration_form import RegistrationForm

import src.clup.flaskr.global_setup as setup
from src.clup.usecases.generic_login_usecase import GenericLoginUsecase
from src.clup.usecases.load_user_usecase import LoadUserUseCase
from src.clup.usecases.user_change_password_usecase \
    import UserChangePasswordUseCase
from .flask_user import FlaskUser
from .forms.change_password import ChangePasswordForm
from .forms.user_login_form import UserLoginForm
from src.clup.usecases.user_register_usecase import UserRegisterUsecase


bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['GET', 'POST'])  # conterrà solo i tre link alle tre diverse register per tipo
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if request.form['submit_button'] == 'User':
            return redirect(url_for('auth.user_register'))
        elif request.form['submit_button'] == 'Admin':
            pass  # do something else
        elif request.form['submit_button'] == 'Store Manager':
            pass  #
    elif request.method == 'GET':
        return render_template('register.html', form=form)


@bp.route('/register/user', methods=['GET', 'POST'])  # conterrà solo i tre link alle tre diverse register per tipo
def user_register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password1.data
        ur = UserRegisterUsecase(setup.user_provider)
        try:
            ur.execute(username, password)
            return redirect(url_for('auth.login'))
        except ValueError:
            flash('Something went wrong', category='danger')
            return redirect(url_for('auth.register'))
    elif form.is_submitted():
        flash("check all fields", category='danger')
    return render_template('user_register.html', form=form)


# TODO def user_register()^^^
# TODO def admin_register()
# TODO def store_manager_register()


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    if form.validate_on_submit():
        gl = GenericLoginUsecase(setup.admin_provider,
                                 setup.user_provider,
                                 setup.store_manager_provider)
        username = form.username.data
        password = form.password.data
        try:
            u_id, logged_type = gl.execute(username, password)
            user = FlaskUser(u_id, logged_type)
            login_user(user)
            if current_user.type == 'user':
                return redirect(url_for('user.home'))
            if current_user.type == 'admin':
                return redirect(url_for('admin.home'))
            if current_user.type == 'store_manager':
                return redirect(url_for('store_manager.home'))
        except ValueError:
            flash('Incorrent credentials', category='danger')
            return redirect(url_for('auth.login'))
    else:
        if form.is_submitted():
            flash('form not valid', category='danger')
    return render_template('login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/account/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        old_password = form.old_password.data
        new_password = form.new_password.data
        # TODO considerare i diversi tipi di current_user
        ucp = UserChangePasswordUseCase(setup.user_provider)
        try:
            ludu = LoadUserUseCase(setup.user_provider)
            username = ludu.execute(current_user.get_id()).username
            ucp.execute(username, old_password, new_password)
            return redirect(url_for('auth.logout'))
        except ValueError:
            flash('Something went wrong', category='danger')
            return redirect(url_for('auth.change_password'))
    else:
        if form.is_submitted():
            flash('form not valid', category='danger')
    return render_template('change_password.html', form=form)
