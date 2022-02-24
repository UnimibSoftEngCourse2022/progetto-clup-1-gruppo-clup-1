import json

from flask import Blueprint, render_template, request, abort, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user

import src.clup.flaskr.global_setup as setup
from src.clup.entities.category import Category

from src.clup.usecases.admin.consume_reservation_usecase \
    import ConsumeReservationUseCase
from src.clup.usecases.filter_aisle_by_categories_usecase import FilterAisleByCategoriesUseCase
from src.clup.usecases.admin.free_reservation_usecase \
    import FreeReservationUseCase
from src.clup.usecases.admin.load_admin_store_info_usecase \
    import LoadAdminStoreInfoUseCase
from src.clup.usecases.admin.load_admin_usecase import LoadAdminUseCase
from src.clup.usecases.make_reservation_usecase import MakeReservationUseCase

bp = Blueprint('admin', __name__)


def check_correct_account_type(requested_type):
    if current_user.type != requested_type:
        return False
    else:
        return True


@bp.route('/admin/home')
@login_required
def home():
    if not check_correct_account_type('admin'):
        flash("unauthorized to visit this page, login as an admin", category='danger')
        return redirect(url_for('auth.login'))
    a_id = current_user.get_id()
    admin_data = LoadAdminUseCase(setup.admin_provider).execute(a_id)
    lasiu = LoadAdminStoreInfoUseCase(setup.store_provider,
                                      setup.aisle_provider,
                                      setup.lane_provider,
                                      setup.admin_provider)
    info = lasiu.execute(a_id)
    return render_template('admin/home.html', admin=admin_data,
                           store=info['store'], aisles=info['aisles'],
                           capacity=info['capacity'], current_people=info['current_people'],
                           enabled=info['enabled'])


@bp.route('/admin/reservations/consumed', methods=['POST', 'DELETE'])
@login_required
def consumed_reservations():
    if not check_correct_account_type('admin'):
        flash("unauthorized to visit this page, login as an admin", category='danger')
        return redirect(url_for('auth.login'))
    store_id = request.values['store_id']
    reservation_id = request.values['reservation_id']

    a_id = current_user.get_id()
    lasiu = LoadAdminStoreInfoUseCase(setup.store_provider,
                                      setup.aisle_provider,
                                      setup.lane_provider,
                                      setup.admin_provider)
    info = lasiu.execute(a_id)
    if info['store'].id != store_id:
        abort(400)

    if request.method == 'POST':
        try:
            cru = ConsumeReservationUseCase(
                setup.lane_provider, setup.reservation_provider)
            cru.execute(store_id, reservation_id)
            return '', 200
        except Exception as e:
            print(e)
            abort(400)
    else:
        try:
            fru = FreeReservationUseCase(
                setup.lane_provider, setup.reservation_provider)
            fru.execute(store_id, reservation_id)
            return '', 200
        except Exception as e:
            print(e)
            abort(400)


@bp.route('/admin/reservations/<store_id>', methods=['POST'])
@login_required
def make_reservation(store_id):
    a_id = current_user.get_id()
    categories = request.values['categories']
    try:
        categories_json = json.loads(categories)

        categories_enum = [Category(int(c)) for c in categories_json]
        fabc = FilterAisleByCategoriesUseCase(setup.aisle_provider)
        aisle_ids_json = fabc.execute(store_id, categories_enum)
    except json.JSONDecodeError:
        abort(400)

    mru = MakeReservationUseCase(setup.lane_provider,
                                 setup.reservation_provider)
    r_id = mru.execute(a_id, store_id, aisle_ids_json)

    for aisle_id in aisle_ids_json:
        pool = setup.lane_provider.get_aisle_pool(aisle_id)
        queue = setup.lane_provider.get_waiting_queue(aisle_id)
        print(f'{aisle_id} - {pool.capacity} - {pool.current_quantity}')
        print(list(queue))
        print(list(pool))
    return jsonify(r_id), 200
