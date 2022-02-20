from flask import Blueprint, render_template
from flask_login import login_user, login_required, current_user

import src.clup.flaskr.global_setup as setup
from src.clup.usecases.load_admin_store_info_usecase \
    import LoadAdminStoreInfoUseCase
from src.clup.usecases.load_admin_usecase import LoadAdminUseCase


bp = Blueprint('admin', __name__)


@bp.route('/admin/home')
@login_required
def home():
    a_id = current_user.get_id()
    admin_data = LoadAdminUseCase(setup.admin_provider).execute(a_id)
    lasiu = LoadAdminStoreInfoUseCase(setup.store_provider,
        setup.aisle_provider, setup.lane_provider, setup.admin_provider)
    info = lasiu.execute(a_id)
    return render_template('admin/home.html', store=info['store'],
        aisles=info['aisles'], capacity=info['capacity'])
