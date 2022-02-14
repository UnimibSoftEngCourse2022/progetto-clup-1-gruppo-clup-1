import json
from json import JSONDecodeError

from flask import Blueprint, redirect, render_template, request, url_for, abort
from flask_login import login_required, current_user

import src.clup.flaskr.global_setup as setup
from src.clup.entities.category import Category
from src.clup.usecases.add_aisle_usecase import AddAisleUseCase
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
aau = AddAisleUseCase(setup.aisle_provider)

mru = MakeReservationUseCase(setup.lane_provider, setup.reservation_provider)
fru = FreeReservationUseCase(setup.lane_provider, setup.reservation_provider)
cru = ConsumeReservationUseCase(
    setup.lane_provider, setup.reservation_provider
)

usu = UpdateStoreUseCase(setup.store_provider, setup.lane_provider)


@bp.route('/stores/init')
@login_required
def init_stores():
    esselunga = asu.execute('Esselunga', 'Campofiorenzo', 1)
    conad = asu.execute('Conad', 'Catania', 10)

    aau.execute(esselunga.id, 'pane', [Category.MEAT])
    aau.execute(esselunga.id, 'pesce', [Category.FISH])
    aau.execute(conad.id, 'salumi', [Category.FRUIT])
    aau.execute(conad.id, 'frutta', [Category.MEAT])

    esselunga_aisle_ids = setup.aisle_provider.get_store_aisle_ids(esselunga.id)
    for aisle_id in esselunga_aisle_ids:
        setup.lane_provider.get_aisle_pool(aisle_id).capacity = 5
    conad_aisle_ids = setup.aisle_provider.get_store_aisle_ids(conad.id)
    for aisle_id in conad_aisle_ids:
        setup.lane_provider.get_aisle_pool(aisle_id).capacity = 5

    return redirect(url_for('stores.show_stores'))


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
                return redirect(url_for('stores.show_store',
                                        store_id=store.id))
    else:
        for store in slu.execute():
            if store.id == store_id:
                pool = setup.lane_provider.get_store_pool(store_id)
                active_pool_len = len(pool.enabled)
                aisle_ids = setup.aisle_provider.get_store_aisle_ids(store_id)
                args = {
                    'store': store,
                    'active_pool_len': active_pool_len,
                    'store_pool_enabled': pool.enabled,
                    'aisle_ids': aisle_ids,
                }
                return render_template('store.html', **args)
        abort(404)


@bp.route('/stores/<store_id>/reservations', methods=['GET', 'POST'])
@login_required
def store_reservations(store_id):
    if request.method == 'POST':
        user_id = current_user.get_id()
        aisle_ids = request.values['aisle_ids']
        try:
            aisle_ids_json = json.loads(aisle_ids)
            print(aisle_ids_json)
        except JSONDecodeError:
            abort(400)
        mru.execute(user_id, store_id, aisle_ids_json)
        return '', 200
    else:
        enabled = setup.lane_provider.get_store_pool(store_id).enabled
        to_free = setup.lane_provider.get_store_pool(store_id).to_free
        return render_template('store_reservations.html',
                               store_id=store_id,
                               enabled_ids=enabled,
                               to_free_ids=to_free)


@bp.route('/stores/<store_id>/consumed', methods=['POST', 'DELETE'])
def store_pool_handler(store_id):
    if request.method == 'POST':
        try:
            reservation_id = request.values['reservation_id']
            cru.execute(store_id, reservation_id)
            return '', 200
        except Exception:
            abort(400)
    else:
        try:
            reservation_id = request.values['reservation_id']
            fru.execute(store_id, reservation_id)
            return '', 200
        except Exception:
            abort(400)
