import json

from flask import Blueprint, abort, flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from src.clup.usecases.store_manager.add_store import AddStore
from src.clup.flaskr import global_setup as setup
from src.clup.flaskr.forms.add_store_form import AddStoreForm
from src.clup.usecases.store_manager.add_aisle import AddAisle
from src.clup.usecases.load_store_info import LoadStoreInfo
from src.clup.usecases.store_manager.load_store_manager import LoadStoreManager
from src.clup.entities.category import Category

bp = Blueprint('store_manager', __name__)
liu = LoadStoreInfo(setup.store_provider, setup.aisle_provider)


def check_correct_account_type(requested_type):
    if current_user.type != requested_type:
        return False
    else:
        return True


@bp.route('/storemanager/home')
@login_required
def home():
    if not check_correct_account_type('store_manager'):
        flash("unauthorized to visit this page, login as a store manager", category='danger')
        return redirect(url_for('auth.login'))
    lsm = LoadStoreManager(setup.store_manager_provider)
    store_manager = lsm.execute(current_user.id)
    stores = setup.store_provider.get_stores_from_manager_id(store_manager.id)
    return render_template('store_manager/home.html', sm=store_manager, stores=stores)


@bp.route('/storemanager/stores/<store_id>')
@login_required
def store_info(store_id):
    if not check_correct_account_type('store_manager'):
        flash("unauthorized to visit this page, login as a store manager", category='danger')
        return redirect(url_for('auth.login'))
    lsm = LoadStoreManager(setup.store_manager_provider)
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
    lsm = LoadStoreManager(setup.store_manager_provider)
    store_manager = lsm.execute(current_user.id)
    if not check_correct_account_type('store_manager'):
        flash("unauthorized to visit this page, login as a store manager", category='danger')
        return redirect(url_for('auth.login'))
    form = AddStoreForm()
    if form.validate_on_submit() and request.method == 'POST':
        store_name = form.name.data
        store_address = form.address.data
        asu = AddStore(setup.store_provider)
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
    if request.method == 'GET':
        return render_template('store_manager/add_store.html', sm=store_manager, form=form)


@bp.route('/storemanager/<store_id>/set_aisles', methods=['GET', 'POST'])
@login_required
def set_aisles(store_id):
    if not check_correct_account_type('store_manager'):
        flash("unauthorized to visit this page, login as a store manager", category='danger')
        return redirect(url_for('auth.login'))
    lsm = LoadStoreManager(setup.store_manager_provider)
    store_manager = lsm.execute(current_user.id)
    if not check_correct_account_type('store_manager'):
        flash("unauthorized to visit this page, login as a store manager", category='danger')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        name = request.values['name']
        capacity = int(request.values['capacity'])
        categories = request.values['categories']
        try:
            categories_json = json.loads(categories)
            categories_enum = [Category(int(c)) for c in categories_json]
            for i in range(100):
                print(categories_enum)
            aau = AddAisle(setup.aisle_provider, setup.lane_provider)
            aau.execute(store_id, name, categories_enum, capacity)
            return redirect(url_for('store_manager.set_aisles', store_id=store_id))
        except json.JSONDecodeError:
            abort(400)

    base_categories = [Category.MEAT, Category.BAKERY, Category.BEAUTY, Category.VEGETABLE, Category.FISH,
                       Category.BEVERAGE, Category.FRUIT, Category.OTHER]
    return render_template('store_manager/set_aisle.html', store_id=store_id, categories=base_categories,
                           sm=store_manager, )
