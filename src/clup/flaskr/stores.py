import json

import flask
from flask import Blueprint, redirect, render_template, request, url_for, abort
from flask_login import login_required, current_user

import src.clup.flaskr.global_setup as setup
from src.clup.usecases.add_store_usecase import AddStoreUseCase
from src.clup.usecases.consume_reservation_usecase \
    import ConsumeReservationUseCase
from src.clup.usecases.free_reservation_usecase import FreeReservationUseCase
from src.clup.usecases.make_reservation_usecase import MakeReservationUseCase
from src.clup.usecases.store_list_usecase import StoreListUseCase
from src.clup.usecases.update_store_usecase import UpdateStoreUseCase

# from src.clup.entities.exceptions \
#     import MaxCapacityReachedError, EmptyQueueError


bp = Blueprint('stores', __name__)

slu = StoreListUseCase(setup.store_provider)

asu = AddStoreUseCase(setup.store_provider, setup.lane_provider)
asu.execute('Esselunga', 'Campofiorenzo', 1)
asu.execute('Conad', 'Catania', 10)

mru = MakeReservationUseCase(setup.lane_provider, setup.reservation_provider)
fru = FreeReservationUseCase(setup.lane_provider, setup.reservation_provider)
cru = ConsumeReservationUseCase(setup.lane_provider, setup.reservation_provider)

usu = UpdateStoreUseCase(setup.store_provider, setup.lane_provider)


@bp.route('/stores', methods=['GET', 'POST'])
@login_required
def show_stores():
    if request.method == 'POST':
        store_name = request.values['name']
        store_address = request.values['address']
        store_capacity = int(request.values['capacity'])
        try:
            store = asu.execute(store_name, store_address, store_capacity)
            return redirect(url_for('stores.show_store', store_id=store.id))
        except ValueError:
            return 'ERROR'
    else:
        stores = slu.execute()
        return render_template('stores.html', stores=stores)


@bp.route('/stores/<store_id>', methods=['GET', 'PUT'])
@login_required
def show_store(store_id):
    if request.method == 'PUT':
        # abort(404)
        for store in slu.execute():
            if store.id == store_id:
                capacity = int(request.values['capacity'])
                usu.execute(store, capacity)
                return redirect(url_for('stores.show_store', store_id=store.id))
    else:
        for store in slu.execute():
            if store.id == store_id:
                pool = setup.lane_provider.get_store_pool(store_id)
                active_pool_len = len(pool.enabled)
                args = {
                    'store': store,
                    'active_pool_len': active_pool_len,
                    'store_pool_enabled': pool.enabled
                }
                return render_template('store.html', **args)
        abort(404)


@bp.route('/stores/<store_id>/reservations', methods=['POST'])
@login_required
def make_reservation(store_id):
    user_id = current_user.get_id()
    aisle_ids = request.values['aisle_ids']
    try:
        aisle_ids_json = json.loads(aisle_ids)
    except JSONDecodeError:
        abort(400)
    mru.execute(user_id, store_id, aisle_ids_json)
    return '', 200


@bp.route('/reservations', methods=['GET'])
@login_required
def show_reservation():
    reservations = setup.reservation_provider.get_reservations()
    return render_template('reservations.html', reservations=reservations)


# @bp.route('/<id>/active_pool', methods=['POST'])
# def enable_reservation_into_store(id):
#     try:
#         eru.execute(id)
#         return redirect(url_for('stores.show_store', id=id))
#     except MaxCapacityReachedError:
#         return 'MAX CAPACITY ERROR'
#     except EmptyQueueError:
#         return 'EMPTY QUEUE ERROR'

@bp.route('/stores/<store_id>/active_pool/<reservation_id>', methods=['DELETE'])
def consume_handler(store_id, reservation_id):
    try:
        # return redirect(url_for('stores.show_store', id=id))
        cru.execute(store_id, reservation_id)
        flask.response(200)
    except Exception:
        return 'ERROR1'


@bp.route('/stores/<store_id>/waiting_queue', methods=['DELETE'])
def delete_reservation_from_waiting_queue(store_id):
    try:
        flask.response(200)
    except Exception:
        flask.response(500)


@bp.route('/stores/<store_id>/active_pool', methods=['DELETE'])
def free_handler(store_id):
    try:
        fru.execute(store_id)
        return '', 200
    except Exception as e:
        return f'Error {e}', 500
