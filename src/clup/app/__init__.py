from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fd27835ea6ab3d57137c0e3e'
app.config['WTF_CSRF_ENABLED'] = True

from app import views