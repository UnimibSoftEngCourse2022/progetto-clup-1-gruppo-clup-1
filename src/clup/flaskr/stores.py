from flask import Blueprint, redirect, render_template, request, url_for, abort
from flask_login import login_required, current_user

import src.clup.flaskr.global_setup as setup
from src.clup.entities.category import Category
from src.clup.usecases.store_manager.add_aisle import AddAisle
from src.clup.usecases.store_manager.add_store import AddStore
from src.clup.usecases.auth.admin_register import AdminRegister
from src.clup.usecases.admin.consume_reservation \
    import ConsumeReservation
from src.clup.usecases.system.create_store_manager import CreateStoreManager
from src.clup.usecases.admin.free_reservation import FreeReservation
from src.clup.usecases.admin.load_admin import LoadAdmin
from src.clup.usecases.make_reservation import MakeReservation
from src.clup.usecases.search_store import SearchStore
from src.clup.usecases.store_list import StoreList
from src.clup.usecases.store_manager.update_store import UpdateStore
from src.clup.usecases.auth.user_register import UserRegister

bp = Blueprint('stores', __name__)

slu = StoreList(setup.store_provider)
asu = AddStore(setup.store_provider)
aau = AddAisle(setup.aisle_provider, setup.lane_provider)
mru = MakeReservation(setup.lane_provider, setup.reservation_provider)
fru = FreeReservation(setup.lane_provider, setup.reservation_provider)
cru = ConsumeReservation(
    setup.lane_provider, setup.reservation_provider
)
usu = UpdateStore(setup.store_provider, setup.lane_provider)
ssu = SearchStore(setup.store_provider)
luau = LoadAdmin(setup.admin_provider)


@bp.route('/data/init')
def init_stores():
    esselunga = asu.execute('Esselunga', 'Campofiorenzo', 1)
    conad = asu.execute('Conad', 'Catania', 10)

    aau.execute(esselunga.id, 'pane', [Category.MEAT])
    aau.execute(esselunga.id, 'pesce', [Category.FISH])
    aau.execute(conad.id, 'salumi', [Category.MEAT, Category.BEVERAGE])
    aau.execute(conad.id, 'frutta', [Category.FRUIT])

    e_aisle_ids = setup.aisle_provider.get_store_aisle_ids(esselunga.id)
    for aisle_id in e_aisle_ids:
        setup.lane_provider.get_aisle_pool(aisle_id).capacity = 5
    c_aisle_ids = setup.aisle_provider.get_store_aisle_ids(conad.id)
    for aisle_id in c_aisle_ids:
        setup.lane_provider.get_aisle_pool(aisle_id).capacity = 5

    uru = UserRegister(setup.user_provider)
    uru.execute('davide', 'prova')

    aru = AdminRegister(setup.admin_provider, setup.store_provider)
    aru.execute('admin1', 'password', esselunga.name, esselunga.address, esselunga.secret)
    aru.execute('admin2', 'password', conad.name, conad.address, conad.secret)

    csm = CreateStoreManager(setup.store_manager_provider)
    csm.execute('secret_key')

    return redirect(url_for('stores.stores'))


@bp.route('/stores', methods=['GET', 'POST'])
@login_required
def stores():
    a_id = current_user.get_id()
    admin_data = luau.execute(a_id)
    if request.method == 'POST':
        store_name = request.values['name']
        store_address = request.values['address']
        store_capacity = int(request.values['capacity'])
        try:
            store = asu.execute(store_name, store_address, store_capacity)
            return redirect(url_for('stores.store', store_id=store.id))
        except ValueError:
            return 'ERROR'
    else:
        stores = slu.execute()
        return render_template('stores.html', stores=stores, admin=admin_data)


@bp.route('/stores/add', methods=['GET'])
@login_required
def add_store():
    stores = slu.execute()
    return render_template('add_store.html', stores=stores)


@bp.route('/stores/<store_id>', methods=['GET', 'PUT'])
@login_required
def store(store_id):
    a_id = current_user.get_id()
    admin_data = luau.execute(a_id)
    if request.method == 'PUT':
        # abort(404)
        for store in slu.execute():
            if store.id == store_id:
                capacity = int(request.values['capacity'])
                usu.execute(store, capacity)
                return redirect(url_for('stores.store', store_id=store.id))
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
                return render_template('store.html', **args, admin=admin_data)
        abort(404)


# @bp.route('/stores/<store_id>/reservations', methods=['GET', 'POST'])
# @login_required
# def reservations(store_id):
#     if request.method == 'POST':
#         user_id = current_user.get_id()
#         aisle_ids = request.values['aisle_ids']
#         try:
#             aisle_ids_json = json.loads(aisle_ids)
#             print(aisle_ids_json)
#         except JSONDecodeError:
#             abort(400)
#         mru.execute(user_id, store_id, aisle_ids_json)
#         return '', 200
#     else:
#         enabled = setup.lane_provider.get_store_pool(store_id).enabled
#         to_free = setup.lane_provider.get_store_pool(store_id).to_free
#         return render_template('store_reservations.html',
#                                store_id=store_id,
#                                enabled_ids=enabled,
#                                to_free_ids=to_free)


# @bp.route('/stores/<store_id>/reservations/consumed',
#           methods=['POST', 'DELETE'])
# def consumed_reservations(store_id):
#     if request.method == 'POST':
#         try:
#             reservation_id = request.values['reservation_id']
#             cru.execute(store_id, reservation_id)
#             return '', 200
#         except Exception:
#             abort(400)
#     else:
#         try:
#             reservation_id = request.values['reservation_id']
#             fru.execute(store_id, reservation_id)
#             return '', 200
#         except Exception:
#             abort(400)


@bp.route('/stores/qr_code_scan', methods=['GET'])
def qrcode():
    return render_template('qr_code_scan_page.html')
