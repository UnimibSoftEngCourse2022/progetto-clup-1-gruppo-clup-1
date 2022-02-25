from flask import Blueprint, render_template, redirect, url_for

import src.clup.flaskr.global_setup as setup
from src.clup.entities.category import Category
from src.clup.usecases.auth.admin_register import AdminRegister
from src.clup.usecases.auth.store_manager_register import StoreManagerRegister
from src.clup.usecases.auth.user_register import UserRegister
from src.clup.usecases.store_manager.add_aisle import AddAisle
from src.clup.usecases.store_manager.add_store import AddStore
from src.clup.usecases.system.create_store_manager import CreateStoreManager

bp = Blueprint('main', __name__)


@bp.route('/home')
@bp.route('/')
def show_home():
    return render_template('home.html')


@bp.route('/init')
def init_stores():
    csm = CreateStoreManager(setup.store_manager_provider)
    sm1_id = csm.execute('secret_key1')
    sm2_id = csm.execute('secret_key2')
    rsm = StoreManagerRegister(setup.store_manager_provider)
    rsm.execute('secret_key1', 'store_manager1@example.clup.com', 'password')
    rsm.execute('secret_key2', 'store_manager2@example.clup.com', 'password')
    asu = AddStore(setup.store_provider)

    esselunga1 = asu.execute('Esselunga', 'Campofiorenzo', sm1_id)
    esselunga2 = asu.execute('Esselunga', 'Albizzate', sm1_id)
    conad = asu.execute('Conad', 'Catania', sm2_id)
    aau = AddAisle(setup.aisle_provider, setup.lane_provider)

    aau.execute(esselunga1.id, 'macelleria', [Category.MEAT])
    aau.execute(esselunga1.id, 'pescheria', [Category.FISH])
    aau.execute(esselunga1.id, 'ortofrutta', [Category.FRUIT, Category.VEGETABLE])
    aau.execute(esselunga2.id, 'pescheria', [Category.FISH])
    aau.execute(esselunga2.id, 'ortofrutta', [Category.FRUIT, Category.VEGETABLE])
    aau.execute(conad.id, 'salumi', [Category.MEAT])
    aau.execute(conad.id, 'ortofrutta', [Category.FRUIT, Category.VEGETABLE])
    aau.execute(conad.id, 'cura personale', [Category.BEAUTY, Category.OTHER])

    e1_aisle_ids = setup.aisle_provider.get_store_aisle_ids(esselunga1.id)
    for aisle_id in e1_aisle_ids:
        setup.lane_provider.get_aisle_pool(aisle_id).capacity = 5
    c_aisle_ids = setup.aisle_provider.get_store_aisle_ids(conad.id)
    for aisle_id in c_aisle_ids:
        setup.lane_provider.get_aisle_pool(aisle_id).capacity = 5

    e2_aisle_ids = setup.aisle_provider.get_store_aisle_ids(esselunga2.id)
    for aisle_id in e2_aisle_ids:
        setup.lane_provider.get_aisle_pool(aisle_id).capacity = 7

    uru = UserRegister(setup.user_provider)
    uru.execute('user@example.clup.com', 'prova')

    aru = AdminRegister(setup.admin_provider, setup.store_provider)
    aru.execute('admin1@example.clup.com', 'password', esselunga1.name, esselunga1.address, esselunga1.secret)
    aru.execute('admin2@example.clup.com', 'password', conad.name, conad.address, conad.secret)
    aru.execute('admin3@example.clup.com', 'password', esselunga2.name, esselunga2.address, esselunga2.secret)

    return redirect(url_for('main.show_home'))
