import flask
import json
from flask import Blueprint, redirect, render_template, request, url_for, abort
from flask_login import login_required, current_user

from src.clup.usecases.load_user_data_usecase import LoadUserDataUseCase
from src.clup.usecases.search_store_usecase import SearchStoreUseCase
from src.clup.usecases.update_store_usecase import UpdateStoreUseCase

from src.clup.flaskr.global_setup import bsp, bqp, brp, bup
from src.clup.usecases.add_store_usecase import AddStoreUseCase
from src.clup.usecases.consume_reservation_usecase \
    import ConsumeReservationUseCase
from src.clup.usecases.free_reservation_usecase import FreeReservationUseCase
from src.clup.usecases.make_reservation_usecase import MakeReservationUseCase
from src.clup.usecases.store_list_usecase import StoreListUseCase

# from src.clup.entities.exceptions \
#     import MaxCapacityReachedError, EmptyQueueError


bp = Blueprint('stores', __name__)

slu = StoreListUseCase(bsp)

asu = AddStoreUseCase(bsp, bqp)
asu.execute('Esselunga', 'Campofiorenzo', 1)
asu.execute('Conad', 'Catania', 10)
asu.execute('Esselunga', 'Milano', 2)
asu.execute('Esselunga', 'Verona', 2)

mru = MakeReservationUseCase(bqp, brp)

fru = FreeReservationUseCase(bqp)

cru = ConsumeReservationUseCase(bqp)

usu = UpdateStoreUseCase(bsp, bqp)

ssu = SearchStoreUseCase(bsp)



@bp.route('/stores', methods=['GET', 'POST'])
@login_required
def show_stores():
    if request.method == 'POST':
        store_name = request.values['name']
        store_address = request.values['address']
        store_capacity = int(request.values['capacity'])
        try:
            store = asu.execute(store_name, store_address, store_capacity)
            return redirect(url_for('stores.show_store', id=store.id))
        except ValueError:
            return 'ERROR'
    else:
        stores = slu.execute()
        return render_template('stores.html', stores=stores)

@bp.route('/stores/add', methods=['GET'])
@login_required
def add_store():
        stores = slu.execute()
        return render_template('add_store.html', stores=stores)


@bp.route('/stores/<id>', methods=['GET', 'PUT'])
@login_required
def show_store(id):
    if request.method == 'PUT':
        # abort(404)
        for store in slu.execute():
            if store.id == id:
                capacity = int(request.values['capacity'])
                usu.execute(store, capacity)
                return redirect(url_for('stores.show_store', id=id))
    else:
        for store in slu.execute():
            if store.id == id:
                pool = bqp.get_active_pool(id)
                active_pool_len = len(pool)
                waiting_queue_len = len(bqp.get_waiting_queue(id))
                current_people_quantity = bqp.get_active_pool(id).current_quantity
                args = {
                    'store': store,
                    'waiting_queue_len': waiting_queue_len,
                    'active_pool_len': active_pool_len,
                    'current_people_quantity': current_people_quantity,
                    'active_pool': pool
                }
                return render_template('store.html', **args)
        abort(404)


@bp.route('/stores/<id>/waiting_queue', methods=['POST'])
@login_required
def make_reservation_into_store(id):
    user_id = current_user.get_id()
    mru.execute(id, user_id)
    return redirect(url_for('stores.show_store', id=id))


@bp.route('/reservations', methods=['GET'])
@login_required
def show_reservation():
    reservations = brp.get_reservations()
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

@bp.route('/stores/qr_code_scan', methods=['GET'])
def qrcode():
    return render_template('qr_code_scan_page.html')

@bp.route('/searchstores/<name>', methods=['POST'])
def search_store(name):
    print(name)
    sl = ssu.execute(name)
    u_id = current_user.get_id()
    user_data = LoadUserDataUseCase(bup).execute(u_id)
    return sl







