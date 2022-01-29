import pathlib
import sys

from flask import Flask


current = pathlib.Path(__file__).resolve()
project_root = current.parent.parent.parent.parent
sys.path.append(str(project_root))


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Register your blueprint here
    from . import stores
    app.register_blueprint(stores.bp)

    return app
