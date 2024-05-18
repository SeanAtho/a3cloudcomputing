from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
import hmac
from flask_login import utils

# Patch the safe_str_cmp function in flask_login.utils
def safe_str_cmp(a, b):
    """Perform a constant time string comparison."""
    return hmac.compare_digest(a, b)

utils.safe_str_cmp = safe_str_cmp

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

try:
    db = SQLAlchemy(app)
except AttributeError as e:
    if "'sqlalchemy' has no attribute '__all__'" in str(e):
        import sqlalchemy
        sqlalchemy.__all__ = []
        db = SQLAlchemy(app)
    else:
        raise e

login_manager = LoginManager(app)
login_manager.login_view = 'login'

from application import routes, models, utils  # Ensure utils is imported

def create_app():
    return app
