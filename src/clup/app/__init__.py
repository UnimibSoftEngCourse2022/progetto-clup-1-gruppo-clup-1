import pathlib
import sys

from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

current = pathlib.Path(__file__).resolve()
project_root = current.parent.parent.parent.parent
sys.path.append(str(project_root))
print(project_root)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'fd27835ea6ab3d57137c0e3e'
csrf = CSRFProtect()
csrf.init_app(app) # Compliant
login_manager = LoginManager()
login_manager.init_app(app)

from app import views

