from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from src.clup.flaskr import global_setup as setup
from src.clup.usecases.add_store_usecase import AddStoreUseCase
from src.clup.usecases.create_store_manager import CreateStoreManagerUseCase
from src.clup.usecases.load_store_info_usecase import LoadStoreInfoUseCase
from src.clup.usecases.load_store_manager_usecase import LoadStoreManagerUseCase
from src.clup.usecases.store_manager_register_usecase import StoreManagerRegisterUseCase

bp = Blueprint('store_manager', __name__)
liu = LoadStoreInfoUseCase(setup.store_provider, setup.aisle_provider)


def check_correct_account_type(requested_type):
    if current_user.type != requested_type:
        return False
    else:
        return True


@bp.route('/manager/data/init')
def data_init():
    csm = CreateStoreManagerUseCase(setup.store_manager_provider)
    id = csm.execute('secret_key')
    rsm = StoreManagerRegisterUseCase(setup.store_manager_provider)
    rsm.execute('secret_key', 'boss', 'prova')
    asu = AddStoreUseCase(setup.store_provider)
    asu.execute('Tigros', 'Solbiate Arno', id)
    asu.execute('Carrefour', 'Jerago', id)
    return redirect(url_for('store_manager.home'))


@bp.route('/storemanager/home')
@login_required
def home():
    if not check_correct_account_type('store_manager'):
        flash(f"unauthorized to visit this page, login as a store manager", category='danger')
        return redirect(url_for('auth.login'))
    lsm = LoadStoreManagerUseCase(setup.store_manager_provider)
    store_manager = lsm.execute(current_user.id)
    stores = setup.store_provider.get_stores_from_manager_id(store_manager.id)
    return render_template('store_manager_home.html', sm=store_manager, stores=stores)


@bp.route('/storemanager/stores/<store_id>')
@login_required
def store_info(store_id):
    store_info = liu.execute(store_id)
    print(store_info)
    return render_template('store_view_manager.html',  store_info=store_info)


@bp.route('/storemanager/stores', methods=['POST'])
@login_required
def create_store():
    # Handle store creation
    pass
