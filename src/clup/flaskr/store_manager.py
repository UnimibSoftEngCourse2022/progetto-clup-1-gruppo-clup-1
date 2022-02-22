from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from src.clup.flaskr import global_setup
from src.clup.usecases.create_store_manager import CreateStoreManagerUseCase
from src.clup.usecases.load_store_manager_usecase import LoadStoreManagerUseCase
from src.clup.usecases.store_manager_register_usecase import StoreManagerRegisterUseCase

bp = Blueprint('store_manager', __name__)


def check_correct_account_type(requested_type):
    if current_user.type != requested_type:
        return False
    else:
        return True


@bp.route('/manager/data/init')
def data_init():
    csm = CreateStoreManagerUseCase(global_setup.store_manager_provider)
    csm.execute('secret_key')
    rsm = StoreManagerRegisterUseCase(global_setup.store_manager_provider)
    rsm.execute('secret_key', 'boss', 'prova')
    return redirect(url_for('store_manager.home'))


@bp.route('/storemanager/home')
@login_required
def home():
    if not check_correct_account_type('store_manager'):
        flash(f"unauthorized to visit this page, login as a store manager", category='danger')
        return redirect(url_for('auth.login'))
    lsm = LoadStoreManagerUseCase(global_setup.store_manager_provider)
    store_manager = lsm.execute(current_user.id)
    return render_template('store_manager_home.html', sm=store_manager)


@bp.route('/storemanager/stores/<store_id>')
@login_required
def store_info(store_id):
    return '<h1>Store Manager Store Info Page</h1>'


@bp.route('/storemanager/stores', methods=['POST'])
@login_required
def create_store():
    # Handle store creation
    pass
