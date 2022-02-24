import json
import datetime

from flask import Blueprint, render_template, request, jsonify, abort, flash, redirect, url_for
from flask_login import login_required, current_user

import src.clup.flaskr.global_setup as setup
from src.clup.entities.category import Category
from src.clup.entities.exceptions import MaxCapacityReachedError
from src.clup.usecases.filter_aisle_by_categories_usecase import FilterAisleByCategoriesUseCase
from src.clup.usecases.get_alternative_stores_usecase import GetAlternativeStoresUseCase
from src.clup.usecases.get_store_categories import GetStoreCategoriesUseCase
from src.clup.usecases.load_store_info_usecase import LoadStoreInfoUseCase
from src.clup.usecases.load_user_usecase import LoadUserUseCase
from src.clup.usecases.load_user_reservations_data_usecase import LoadUserReservationsDataUseCase
from src.clup.usecases.load_user_appointments_data import LoadUserAppointmentsData
from src.clup.usecases.make_appointment_usecase import MakeAppointmentUseCase
from src.clup.usecases.make_reservation_usecase import MakeReservationUseCase
from src.clup.usecases.search_store_usecase import SearchStoreUseCase

bp = Blueprint('user', __name__)


@bp.route('/user/home')
@login_required
def home():
    u_id = current_user.get_id()
    user_data = LoadUserUseCase(setup.user_provider).execute(u_id)
    return render_template('user/home.html', user=user_data)


@bp.route('/user/account')
@login_required
def account():
    return '<h1>User Account Page</h1>'


@bp.route('/user/stores')
@login_required
def search_stores():
    args = request.args
    name = args.get('name', default='', type=str)
    u = SearchStoreUseCase(setup.store_provider)
    store_list = u.execute(name)
    return jsonify(store_list)


@bp.route('/user/stores/<store_id>')
@login_required
def store_info(store_id):
    u_id = current_user.get_id()
    user_data = LoadUserUseCase(setup.user_provider).execute(u_id)
    u = LoadStoreInfoUseCase(setup.store_provider, setup.aisle_provider)
    info = u.execute(store_id)
    gsc = GetStoreCategoriesUseCase(setup.aisle_provider)
    categories = gsc.execute(store_id)
    return render_template('user/store.html', user=user_data,
                           store=info['store'], aisles=info['aisles'], categories=categories)


@bp.route('/user/stores/<store_id>/slots')
@login_required
def store_time_slots(store_id):
    return '<h1>User Store Time Slots Page</h1>'


@bp.route('/user/reservations/<store_id>', methods=['POST'])
@login_required
def make_reservation(store_id):
    user_id = current_user.get_id()
    categories = request.values['categories']
    try:
        categories_json = json.loads(categories)
        categories_enum = [Category(int(c)) for c in categories_json]
        fabc = FilterAisleByCategoriesUseCase(setup.aisle_provider)
        aisle_ids_json = fabc.execute(store_id, categories_enum)
    except json.JSONDecodeError:
        abort(400)

    mru = MakeReservationUseCase(setup.lane_provider,
                                 setup.reservation_provider)
    mru.execute(user_id, store_id, aisle_ids_json)
    for aisle_id in aisle_ids_json:
        pool = setup.lane_provider.get_aisle_pool(aisle_id)
        queue = setup.lane_provider.get_waiting_queue(aisle_id)
        print(f'{aisle_id} - {pool.capacity} - {pool.current_quantity}')
        print(list(queue))
        print(list(pool))
    return '', 200


@bp.route('/user/reservations')
@login_required
def reservations():
    u_id = current_user.get_id()
    user_data = LoadUserUseCase(setup.user_provider).execute(u_id)
    lurdu = LoadUserReservationsDataUseCase(setup.reservation_provider,
                                            setup.store_provider,
                                            setup.aisle_provider,
                                            setup.appointment_provider)
    stores_with_aisles = lurdu.execute(u_id)
    return render_template('user/reservations.html', user=user_data,
                           stores_with_aisles=stores_with_aisles)

@bp.route('/user/appointments')
@login_required
def appointments():
    u_id = current_user.get_id()
    user_data = LoadUserUseCase(setup.user_provider).execute(u_id)
    luad = LoadUserAppointmentsData(
                                   setup.store_provider,
                                   setup.appointment_provider)
    appointments_with_stores = luad.execute(u_id)
    return render_template('user/appointments.html', user=user_data,
                           appointments_with_stores=appointments_with_stores)


@bp.route('/user/stores/<store_id>/appointment', methods=['GET', 'POST'])
@login_required
def make_appointment(store_id):
    u_id = current_user.get_id()
    user_data = LoadUserUseCase(setup.user_provider).execute(u_id)
    u = LoadStoreInfoUseCase(setup.store_provider, setup.aisle_provider)
    info = u.execute(store_id)
    gsc = GetStoreCategoriesUseCase(setup.aisle_provider)
    categories_from_use_case = gsc.execute(store_id)
    if request.method == 'POST':
        try:
            categories = request.values['categories']
            categories_json = json.loads(categories)
            categories_enum = [Category(int(c)) for c in categories_json]
            fabc = FilterAisleByCategoriesUseCase(setup.aisle_provider)
            aisle_ids_json = fabc.execute(store_id, categories_enum)
            date_str = request.values['date']
            hour = request.values['hour']
            year, month, day = date_str.split('-')
            mauc = MakeAppointmentUseCase(reservation_provider=setup.reservation_provider,
                                          appointment_provider=setup.appointment_provider,
                                          aisle_provider=setup.aisle_provider)
            now = datetime.datetime.now()
            selected_date = datetime.datetime(int(year), int(month), int(day), int(hour), 0, 0)
            if selected_date < now:
                flash('selected date is past current datetime', category='danger')
                return '', 402
        except json.JSONDecodeError:
            abort(400)

        except ValueError:
            flash("insert a correct value", category='danger')
            return '', 402
        try:
            mauc.execute(
                store_id=store_id,
                aisle_ids=aisle_ids_json,
                date=selected_date,
                user_id=u_id
            )
            return '', 200
        except MaxCapacityReachedError:
            return "max_capacity", 401

    return render_template('user/appointment.html', user=user_data, store_id=store_id, store=info['store'],
                           categories=categories_from_use_case)


@bp.route('/user/stores/appointment/alternative')
@login_required
def alternative_appointment():
    args = request.args
    try:
        categories_str = args['categories']
        categories_list = categories_str.split(',')
        categories_enum = [Category(int(c)) for c in categories_list[:-1]]
        date_str = request.values['date']
        hour = request.values['hour']
        year, month, day = date_str.split('-')
        date_time = datetime.datetime(int(year), int(month), int(day), int(hour))
        gasu = GetAlternativeStoresUseCase(setup.store_provider, setup.aisle_provider, setup.reservation_provider,
                                           setup.appointment_provider)
        alt_stores = gasu.execute(categories_enum, date_time)
        if len(alt_stores) == 0:
            return render_template("no_alternative_stores.html")
        else:
            return render_template("valid_stores.html", stores=alt_stores, date=date_str,
             hour=hour, categories_enum = categories_enum, date_time = date_str, categories = categories_str[:-1])
    except ValueError:
        flash("something went wrong", category='danger')
        return redirect(url_for('user.home'))
