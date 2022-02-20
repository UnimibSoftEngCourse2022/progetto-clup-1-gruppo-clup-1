from flask import Blueprint
from flask_login import login_required


bp = Blueprint('store_manager', __name__)


@bp.route('/storemanager/home')
@login_required
def home():
    return '<h1>Store Manager Home Page</h1>'


@bp.route('/storemanager/stores/<store_id>')
@login_required
def store_info(store_id):
    return '<h1>Store Manager Store Info Page</h1>'


@bp.route('/storemanager/stores', methods=['POST'])
@login_required
def create_store():
    # Handle store creation
    pass
