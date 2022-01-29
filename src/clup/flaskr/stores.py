from flask import Blueprint

from src.clup.providers.basic_store_provider import BasicStoreProvider


bp = Blueprint('stores', __name__, url_prefix='/stores')

bsp = BasicStoreProvider()

@bp.route('/store1')
def show_store():
    return '<h1>Hello, World!</h1>'

