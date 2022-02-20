from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user

import src.clup.flaskr.global_setup as setup
from src.clup.usecases.load_store_info_usecase import LoadStoreInfoUseCase
from src.clup.usecases.load_user_usecase import LoadUserUseCase
from src.clup.usecases.search_store_usecase import SearchStoreUseCase


bp = Blueprint('user', __name__)


@bp.route('/user/home')
@login_required
def home():
    u_id = current_user.get_id()
    user_data = LoadUserUseCase(setup.user_provider).execute(u_id)
    return render_template('user/home.html', user=user_data)


@bp.route('/user/account')
@login_required
def account():
    return '<h1>User Account Page</h1>'


@bp.route('/user/stores')
@login_required
def search_stores():
    args = request.args
    name = args.get('name', default='', type=str)
    u = SearchStoreUseCase(setup.store_provider)
    store_list = u.execute(name)
    return jsonify(store_list)


@bp.route('/user/stores/<store_id>')
@login_required
def store_info(store_id):
    u_id = current_user.get_id()
    user_data = LoadUserUseCase(setup.user_provider).execute(u_id)
    u = LoadStoreInfoUseCase(setup.store_provider, setup.aisle_provider)
    info = u.execute(store_id)
    return render_template('user/store.html', user=user_data,
                           store=info['store'], aisles=info['aisles'])


@bp.route('/user/stores/<store_id>/slots')
@login_required
def store_time_slots(store_id):
    return '<h1>User Store Time Slots Page</h1>'


@bp.route('/user/reservations')
@login_required
def reservations():
    u_id = current_user.get_id()
    user_data = LoadUserUseCase(setup.user_provider).execute(u_id)
    reservations = setup.reservation_provider.get_user_reservations(u_id)
    return render_template('user/reservations.html', user=user_data,
                           reservations=reservations)
