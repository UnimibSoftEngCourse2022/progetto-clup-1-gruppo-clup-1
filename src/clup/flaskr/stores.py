from flask import Blueprint, redirect, render_template, request, url_for

from src.clup.usecases.store_list_usecase import StoreListUseCase
from src.clup.providers.basic_queue_provider import BasicQueueProvider
from src.clup.usecases.add_store_usecase import AddStoreUseCase
from src.clup.providers.basic_store_provider import BasicStoreProvider


bp = Blueprint('stores', __name__, url_prefix='/stores')


bsp = BasicStoreProvider()
bqp = BasicQueueProvider()

slu = StoreListUseCase(bsp)

asu = AddStoreUseCase(bsp, bqp)
asu.execute('Esselunga', 'Campofiorenzo', 1)
asu.execute('Conad', 'Catania', 10)


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
            return render_template('store.html', store=store)


@bp.route('/<id>/waiting_queue/reservation', methods=['POST'])
def make_reservation_into_store(id):
    pass


@bp.route('/<id>/active_pool/reservation', methods=['POST'])
def enable_reservation_into_store(id):
    pass
