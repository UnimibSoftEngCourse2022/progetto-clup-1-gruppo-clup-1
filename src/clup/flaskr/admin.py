from flask import Blueprint, render_template, request, abort
from flask_login import login_required, current_user

import src.clup.flaskr.global_setup as setup
from src.clup.usecases.load_admin_store_info_usecase \
    import LoadAdminStoreInfoUseCase
from src.clup.usecases.load_admin_usecase import LoadAdminUseCase
from src.clup.usecases.consume_reservation_usecase \
    import ConsumeReservationUseCase
from src.clup.usecases.free_reservation_usecase \
    import FreeReservationUseCase


bp = Blueprint('admin', __name__)


@bp.route('/admin/home')
@login_required
def home():
    a_id = current_user.get_id()
    admin_data = LoadAdminUseCase(setup.admin_provider).execute(a_id)
    lasiu = LoadAdminStoreInfoUseCase(setup.store_provider,
                                      setup.aisle_provider,
                                      setup.lane_provider,
                                      setup.admin_provider)
    info = lasiu.execute(a_id)
    return render_template('admin/home.html', admin=admin_data,
                           store=info['store'], aisles=info['aisles'],
                           capacity=info['capacity'])


@bp.route('/admin/reservations/consumed', methods=['POST', 'DELETE'])
@login_required
def consumed_reservations():
    store_id = request.values['store_id']
    reservation_id = request.values['reservation_id']

    a_id = current_user.get_id()
    lasiu = LoadAdminStoreInfoUseCase(setup.store_provider,
                                      setup.aisle_provider,
                                      setup.lane_provider,
                                      setup.admin_provider)
    info = lasiu.execute(a_id)
    if info['store'].id != store_id:
        abort(400)

    if request.method == 'POST':
        try:
            cru = ConsumeReservationUseCase(
                setup.lane_provider, setup.reservation_provider)
            cru.execute(store_id, reservation_id)
            return '', 200
        except Exception:
            abort(400)
    else:
        try:
            fru = FreeReservationUseCase(
                setup.lane_provider, setup.reservation_provider)
            fru.execute(store_id, reservation_id)
            return '', 200
        except Exception:
            abort(400)
