from flask import Flask
from flask_wtf.csrf import CSRFProtect

from pathlib import Path
import sys, os
from os.path import dirname


sys.path.append(dirname(__file__)[:-13].replace('\\', '/'))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'fd27835ea6ab3d57137c0e3e'
csrf = CSRFProtect()
csrf.init_app(app) # Compliant


from app import views
