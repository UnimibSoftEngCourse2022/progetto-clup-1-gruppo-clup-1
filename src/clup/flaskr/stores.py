from flask import Blueprint, redirect, render_template, request, url_for, abort
import flask

from src.clup.usecases.free_reservation_usecase import FreeReservationUseCase
from src.clup.usecases.make_reservation_usecase import MakeReservationUseCase
from src.clup.usecases.consume_reservation_usecase \
    import ConsumeReservationUseCase
from src.clup.providers.basic_reservation_provider \
    import BasicReservationProvider
from src.clup.usecases.store_list_usecase import StoreListUseCase
from src.clup.providers.basic_queue_provider import BasicQueueProvider
from src.clup.usecases.add_store_usecase import AddStoreUseCase
from src.clup.providers.basic_store_provider import BasicStoreProvider
# from src.clup.entities.exceptions \
#     import MaxCapacityReachedError, EmptyQueueError


bp = Blueprint('stores', __name__, url_prefix='/stores')


bsp = BasicStoreProvider()
bqp = BasicQueueProvider()
brp = BasicReservationProvider()

slu = StoreListUseCase(bsp)

asu = AddStoreUseCase(bsp, bqp)
asu.execute('Esselunga', 'Campofiorenzo', 1)
asu.execute('Conad', 'Catania', 10)

mru = MakeReservationUseCase(bqp, brp)

fru = FreeReservationUseCase(bqp)

cru = ConsumeReservationUseCase(bqp)


@bp.route('', methods=['GET', 'POST'])
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


@bp.route('/<id>', methods=['GET'])
def show_store(id):
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


@bp.route('/<id>/waiting_queue', methods=['POST'])
def make_reservation_into_store(id):
    mru.execute(id, 12)
    return redirect(url_for('stores.show_store', id=id))


# @bp.route('/<id>/active_pool', methods=['POST'])
# def enable_reservation_into_store(id):
#     try:
#         eru.execute(id)
#         return redirect(url_for('stores.show_store', id=id))
#     except MaxCapacityReachedError:
#         return 'MAX CAPACITY ERROR'
#     except EmptyQueueError:
#         return 'EMPTY QUEUE ERROR'

@bp.route('/<store_id>/active_pool/<reservation_id>', methods=['DELETE'])
def consume_handler(store_id, reservation_id):
    try:
        # return redirect(url_for('stores.show_store', id=id))
        cru.execute(store_id, reservation_id)
        flask.response(200)
    except Exception:
        return 'ERROR1'


@bp.route('/<store_id>/waiting_queue', methods=['DELETE'])
def delete_reservation_from_waiting_queue(store_id):
    try:
        flask.response(200)
    except Exception:
        flask.response(500)


@bp.route('/<store_id>/active_pool', methods=['DELETE'])
def free_handler(store_id):
    try:
        fru.execute(store_id)
        return '', 200
    except Exception as e:
        return f'Error {e}', 500