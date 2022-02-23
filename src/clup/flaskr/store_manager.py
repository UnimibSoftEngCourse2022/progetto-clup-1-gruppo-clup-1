import json

from flask import Blueprint, abort, flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user

from src.clup.entities.category import Category
from src.clup.flaskr import global_setup as setup
from src.clup.flaskr.forms.add_store_form import AddStoreForm
from src.clup.usecases.add_aisle_usecase import AddAisleUseCase
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
    tigros = asu.execute('Tigros', 'Solbiate Arno', id)
    asu.execute('Carrefour', 'Jerago', id)
    aau = AddAisleUseCase(setup.aisle_provider, setup.lane_provider)
    aau.execute(tigros.id, 'aisle1', [Category.FISH, Category.MEAT])
    aau.execute(tigros.id, 'aisle2', [Category.FISH, Category.MEAT])
    aau.execute(tigros.id, 'aisle3', [Category.FISH, Category.MEAT])
    aau.execute(tigros.id, 'aisle4', [Category.FISH, Category.MEAT])
    aau.execute(tigros.id, 'aisle5', [Category.FISH, Category.MEAT])
    aau.execute(tigros.id, 'aisle6', [Category.FISH, Category.MEAT])
    aau.execute(tigros.id, 'aisle7', [Category.FISH, Category.MEAT])
    aau.execute(tigros.id, 'aisle8', [Category.FISH, Category.MEAT])
    aau.execute(tigros.id, 'aisle9', [Category.FISH, Category.MEAT])

    return redirect(url_for('store_manager.home'))


@bp.route('/storemanager/home')
@login_required
def home():
    if not check_correct_account_type('store_manager'):
        flash("unauthorized to visit this page, login as a store manager", category='danger')
        return redirect(url_for('auth.login'))
    lsm = LoadStoreManagerUseCase(setup.store_manager_provider)
    store_manager = lsm.execute(current_user.id)
    stores = setup.store_provider.get_stores_from_manager_id(store_manager.id)
    return render_template('store_manager/store_manager_home.html', sm=store_manager, stores=stores)


@bp.route('/storemanager/stores/<store_id>')
@login_required
def store_info(store_id):
    if not check_correct_account_type('store_manager'):
        flash("unauthorized to visit this page, login as a store manager", category='danger')
        return redirect(url_for('auth.login'))
    lsm = LoadStoreManagerUseCase(setup.store_manager_provider)
    store_manager = lsm.execute(current_user.id)
    store_info = liu.execute(store_id)
    print(store_info)
    return render_template('store_manager/store_view_manager.html', sm=store_manager, store_info=store_info)


@bp.route('/storemanager/add_store', methods=['GET', 'POST'])
@login_required
def add_store():
    if not check_correct_account_type('store_manager'):
        flash("unauthorized to visit this page, login as a store manager", category='danger')
        return redirect(url_for('auth.login'))
    lsm = LoadStoreManagerUseCase(setup.store_manager_provider)
    store_manager = lsm.execute(current_user.id)

    form = AddStoreForm()
    if form.validate_on_submit():
        store_name = form.name.data
        store_address = form.address.data
        asu = AddStoreUseCase(setup.store_provider)
        id = current_user.id
        try:
            store = asu.execute(store_name, store_address, id)
            return redirect(url_for('store_manager.set_aisles', store_id=store.id))
        except ValueError:
            flash('Unable to add store')
            return redirect(url_for('store_manager.home'))
    else:
        if form.is_submitted():
            flash('form not valid', category='danger')
    return render_template('store_manager/add_store.html', sm=store_manager, form=form)


@bp.route('/storemanager/<store_id>/set_aisles', methods=['GET', 'POST'])
@login_required
def set_aisles(store_id):
    if not check_correct_account_type('store_manager'):
        flash("unauthorized to visit this page, login as a store manager", category='danger')
        return redirect(url_for('auth.login'))
    lsm = LoadStoreManagerUseCase(setup.store_manager_provider)
    store_manager = lsm.execute(current_user.id)

    if request.method == 'POST':
        name = request.values['name']
        capacity = int(request.values['capacity'])
        categories = request.values['categories']
        try:
            categories_json = json.loads(categories)
            categories_enum = [Category(int(c)) for c in categories_json]
            for i in range(100):
                print(categories_enum)
            aau = AddAisleUseCase(setup.aisle_provider, setup.lane_provider)
            aau.execute(store_id, name, categories_enum, capacity)
            return redirect(url_for('store_manager.set_aisles', store_id=store_id))
        except json.JSONDecodeError:
            abort(400)

    base_categories = [Category.MEAT, Category.BAKERY, Category.BEAUTY, Category.VEGETABLE, Category.FISH,
                       Category.BEVERAGE, Category.FRUIT, Category.OTHER]
    return render_template('store_manager/set_aisle.html', store_id=store_id, categories=base_categories,
                           sm=store_manager, )
