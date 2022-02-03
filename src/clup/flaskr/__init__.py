import pathlib
import sys

from flask import Flask, flash, redirect, url_for
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect


current = pathlib.Path(__file__).resolve()
project_root = current.parent.parent.parent.parent
sys.path.append(str(project_root))



login_manager = LoginManager()


@login_manager.user_loader
def load_user(u_id):
    from src.clup.providers.basic_user_provider import BasicUserProvider
    from src.clup.providers.basic_admin_provider import BasicAdminProvider

    bup = BasicUserProvider()
    bap = BasicAdminProvider()

    users = bup.get_users()
    admins = bap.get_admins()
    if u_id in [user.id for user in users]:
        return FlaskUser(u_id)
    elif u_id in [admin.id for admin in admins]:
        return FlaskUser(u_id)
    else:
        return None


@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("you must login first", category='danger')
    return redirect(url_for('users.user_login_page'))


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'fd27835ea6ab3d57137c0e3e'

    # Register your blueprint here
    from . import stores
    from . import users
    app.register_blueprint(stores.bp)
    app.register_blueprint(users.bp)

    # Flask mechanism to handle login sessions
    login_manager.init_app(app)

    # SonarCloud CSRF Protection Requirements
    csrf = CSRFProtect()
    csrf.init_app(app)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    return app
