from flask import (
    Blueprint,
    render_template,
    url_for,
    redirect,
)
from flask_login import login_required, current_user

import src.clup.flaskr.global_setup as setup
from src.clup.usecases.load_admin_usecase import LoadAdminUseCase
from src.clup.usecases.load_user_usecase import LoadUserUseCase
from src.clup.usecases.search_store_usecase import SearchStoreUseCase

from .forms.user_reservation_form import UserReservationForm
from src.clup.usecases.make_reservation_usecase import MakeReservationUseCase


bp = Blueprint('users', __name__)

mru = MakeReservationUseCase(setup.lane_provider, setup.reservation_provider)
ssu = SearchStoreUseCase(setup.store_provider)


@bp.route('/reservation/<store_id>', methods=['GET', 'POST'])
def user_reservation(store_id):
    u_id = current_user.get_id()
    user_data = LoadUserUseCase(setup.user_provider).execute(u_id)
    form = UserReservationForm()

    if form.validate_on_submit():
        reservation = mru.execute(store_id, u_id)
        return redirect(url_for('users.user_make_reservation', store_id=store_id, user=user_data, form=form, reservation_id=reservation.id))

    return render_template('user_reservation.html', store=store_id, user=user_data, form=form)


@bp.route('/reservation/<store_id>/<reservation_id>', methods=['GET', 'POST'])
def user_make_reservation(store_id, reservation_id):
    u_id = current_user.get_id()
    user_data = LoadUserUseCase(setup.user_provider).execute(u_id)
    form = UserReservationForm()
    return render_template('user_reservation.html', store=store_id, user=user_data, form=form, reservation_id=reservation_id)


@bp.route('/admin/account')
@login_required
def admin_page():
    a_id = current_user.get_id()
    admin_data = LoadAdminUseCase(setup.admin_provider).execute(a_id)
    return render_template('admin.html', admin=admin_data)
