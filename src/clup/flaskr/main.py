from flask import Blueprint, render_template


bp = Blueprint('main', __name__)


@bp.route('/', methods=['GET'])
def show_home():
    return render_template('home.html')
