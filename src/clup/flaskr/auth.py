from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user

from src.clup.usecases.auth.admin_register import AdminRegister

import src.clup.flaskr.global_setup as setup
from src.clup.usecases.auth.generic_login import GenericLogin
from src.clup.usecases.auth.store_manager_register import StoreManagerRegister
from src.clup.usecases.auth.change_password import ChangePassword
from src.clup.usecases.auth.user_register import UserRegister
from src.clup.usecases.auth.validate_email import ValidateEmail
from .flask_user import FlaskUser
from .forms.admin_register_form import AdminRegisterForm
from .forms.change_password import ChangePasswordForm
from .forms.store_manager_register_form import StoreManagerRegisterForm
from .forms.user_login_form import UserLoginForm
from .forms.user_register_form import UserRegisterForm

bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['GET'])  # conterrà solo i tre link alle tre diverse register per tipo
def register():
    return render_template('auth/register.html')


@bp.route('/register/user', methods=['GET', 'POST'])
def user_register():
    form = UserRegisterForm()
    if form.validate_on_submit() and request.method == 'POST':
        username = form.username.data
        password = form.password1.data
        ve = ValidateEmail()
        if not ve.execute(username):
            flash('username is not a valid email', category='danger')
            return redirect(url_for('auth.user_register'))
        ur = UserRegister(setup.user_provider)
        try:
            ur.execute(username, password)
            return redirect(url_for('auth.login'))
        except ValueError:
            flash('Something went wrong', category='danger')
            return redirect(url_for('auth.user_register'))
    elif form.is_submitted():
        flash("check all fields", category='danger')
        return redirect(url_for('auth.user_register'))
    elif request.method == 'GET':
        return render_template('auth/user_register.html', form=form)


@bp.route('/register/admin', methods=['GET', 'POST'])
def admin_register():
    form = AdminRegisterForm()
    if form.validate_on_submit() and request.method == 'POST':
        username = form.username.data
        password = form.password1.data
        ve = ValidateEmail()
        if not ve.execute(username):
            flash('username is not a valid email', category='danger')
            return redirect(url_for('auth.admin_register'))
        store_name = form.store_name.data
        store_address = form.store_address.data
        store_sk = form.store_sk.data
        ar = AdminRegister(setup.admin_provider, setup.store_provider)
        try:
            ar.execute(username, password, store_name, store_address, store_sk)
            return redirect(url_for('auth.login'))
        except ValueError:
            flash('Something went wrong', category='danger')
            return redirect(url_for('auth.admin_register'))
    elif form.is_submitted():
        flash("check all fields", category='danger')
    elif request.method == 'GET':
        return render_template('auth/admin_register.html', form=form)


@bp.route('/register/store_manager',
          methods=['GET', 'POST'])  # conterrà solo i tre link alle tre diverse register per tipo
def store_manager_register():
    form = StoreManagerRegisterForm()
    if form.validate_on_submit() and request.method == 'POST':
        username = form.username.data
        ve = ValidateEmail()
        if not ve.execute(username):
            flash('username is not a valid email', category='danger')
            return redirect(url_for('auth.store_manager_register'))
        password = form.password1.data
        secret_key = form.secret_key.data
        smr = StoreManagerRegister(setup.store_manager_provider)
        try:
            smr.execute(secret_key, username, password)
            return redirect(url_for('auth.login'))
        except ValueError:
            flash('Something went wrong', category='danger')
            return redirect(url_for('auth.store_manager_register'))
    elif form.is_submitted():
        flash("check all fields", category='danger')
    elif request.method == 'GET':
        return render_template('auth/store_manager_register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    if form.validate_on_submit() and request.method == 'POST':
        gl = GenericLogin(setup.admin_provider,
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
    if request.method == 'GET':
        return render_template('auth/login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/account/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit() and request.method == 'POST':
        old_password = form.old_password.data
        new_password = form.new_password.data
        # TODO considerare i diversi tipi di current_user
        ucp = ChangePassword(setup.user_provider,
                             setup.admin_provider,
                             setup.store_manager_provider)
        try:
            ucp.execute(current_user.id, old_password, new_password)
            return redirect(url_for('auth.logout'))
        except ValueError:
            flash('Something went wrong', category='danger')
            return redirect(url_for('auth.change_password'))
    else:
        if form.is_submitted():
            flash('form not valid', category='danger')
    if request.method == 'GET':
        return render_template('auth/change_password.html', form=form)
