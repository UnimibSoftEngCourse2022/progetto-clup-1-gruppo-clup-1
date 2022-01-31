from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.config['SECRET_KEY'] = 'fd27835ea6ab3d57137c0e3e'
csrf = CSRFProtect()
csrf.init_app(app) # Compliant
login_manager = LoginManager()
login_manager.init_app(app)

from app import views

