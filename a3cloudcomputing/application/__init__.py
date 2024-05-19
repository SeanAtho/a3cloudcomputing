from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
import hmac
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/flask_social_app.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

# Patch the safe_str_cmp function in flask_login.utils
def safe_str_cmp(a, b):
    """Perform a constant time string comparison."""
    return hmac.compare_digest(a, b)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql+pymysql://SeanAtt03:3DHUMafHiNipUhPi37pE@awseb-e-zvx4mce2hh-stack-awsebrdsdatabase-imgcu2es8qnf.c9a8y6kmk0u7.ap-southeast-2.rds.amazonaws.com:3306/ebdb')
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

from application import routes, models, utils

# Log application startup
logger.info('Flask Social App startup')

def create_app():
    return app
