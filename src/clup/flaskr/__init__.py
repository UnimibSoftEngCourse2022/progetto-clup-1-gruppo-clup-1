import datetime
import pathlib
import sys

from flask import Flask, flash, redirect, url_for
from flask_apscheduler import APScheduler
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

current = pathlib.Path(__file__).resolve()
project_root = current.parent.parent.parent.parent
sys.path.append(str(project_root))

login_manager = LoginManager()


@login_manager.user_loader
def load_user(u_id):
    from src.clup.flaskr.global_setup import user_provider, admin_provider, store_manager_provider
    from src.clup.flaskr.flask_user import FlaskUser

    users = user_provider.get_users()
    admins = admin_provider.get_admins()
    managers = store_manager_provider.get_store_managers()
    if u_id in [user.id for user in users]:
        return FlaskUser(u_id, 'user')
    elif u_id in [admin.id for admin in admins]:
        return FlaskUser(u_id, 'admin')
    elif u_id in [sm.id for sm in managers]:
        return FlaskUser(u_id, 'store_manager')
    else:
        return None


@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("you must login first", category='danger')
    return redirect(url_for('auth.login'))


def activate_appointment():
    from src.clup.usecases.scheduler_usecase import SchedulerUseCase
    from src.clup.flaskr.global_setup import appointment_provider, lane_provider, reservation_provider

    date_time = datetime.datetime.now()
    date_time = datetime.datetime(
        year=date_time.year,
        month=date_time.month,
        day=date_time.day,
        hour=date_time.hour
    )
    suc = SchedulerUseCase(
        appointment_provider=appointment_provider,
        reservation_provider=reservation_provider,
        lane_provider=lane_provider
    )
    suc.execute(date_time)


def remove_unused_reservation_scheduler():
    from src.clup.usecases.remove_unused_reservation import RemoveUnusedReservation
    from src.clup.flaskr.global_setup import store_provider, lane_provider, reservation_provider

    rur = RemoveUnusedReservation(
        store_provider=store_provider,
        lane_provider=lane_provider,
        reservation_provider=reservation_provider
    )
    rur.execute()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'fd27835ea6ab3d57137c0e3e'

    # Flask mechanism to handle login sessions
    login_manager.init_app(app)

    # Register your blueprint here
    from . import stores
    from . import users
    from . import main
    from . import auth
    from . import store_manager
    from . import admin
    from . import user
    app.register_blueprint(stores.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(store_manager.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(user.bp)

    # SonarCloud CSRF Protection Requirements
    csrf = CSRFProtect()
    csrf.init_app(app)

    # Scheduler set up
    app.config['SCHEDULER_API_ENABLED'] = True
    app.config['JOBS'] = [
        {
            "id": "job1",
            "func": "src.clup.flaskr:activate_appointment",
            "args": (),
            "trigger": "interval",
            "seconds": 10,
        },
        {
            "id": "job2",
            "func": "src.clup.flaskr:remove_unused_reservation_scheduler",
            "args": (),
            "trigger": "interval",
            "seconds": 1800,
        }

    ]

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    return app
