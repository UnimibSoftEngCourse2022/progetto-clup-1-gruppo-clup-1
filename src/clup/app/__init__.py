from flask import Flask
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.config['SECRET_KEY'] = 'fd27835ea6ab3d57137c0e3e'
csrf = CSRFProtect()
csrf.init_app(app) # Compliant


from app import views

