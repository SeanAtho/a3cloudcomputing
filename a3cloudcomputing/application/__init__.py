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
# Create a rotating file handler to manage log files
file_handler = RotatingFileHandler('logs/flask_social_app.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)

# Set up the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

# Patch the safe_str_cmp function in flask_login.utils
def safe_str_cmp(a, b):
    """
    Perform a constant time string comparison.

    This function is used to mitigate timing attacks by ensuring that string comparisons
    take a constant amount of time regardless of the input.
    
    Args:
        a (str): The first string to compare.
        b (str): The second string to compare.
    
    Returns:
        bool: True if the strings are equal, False otherwise.
    """
    return hmac.compare_digest(a, b)

# Initialize Flask app
app = Flask(__name__)

# Set up secret key and database URI
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 
    'mysql+pymysql://SeanAtt03:3DHUMafHiNipUhPi37pE@awseb-e-zvx4mce2hh-stack-awsebrdsdatabase-imgcu2es8qnf.c9a8y6kmk0u7.ap-southeast-2.rds.amazonaws.com:3306/ebdb'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
try:
    db = SQLAlchemy(app)
except AttributeError as e:
    # Handle potential attribute error due to SQLAlchemy version compatibility
    if "'sqlalchemy' has no attribute '__all__'" in str(e):
        import sqlalchemy
        sqlalchemy.__all__ = []
        db = SQLAlchemy(app)
    else:
        raise e

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Import application components
from application import routes, models, utils

# Log application startup
logger.info('Flask Social App startup')

def create_app():
    """
    Factory function to create and configure the Flask app.

    This function initializes the Flask app, sets up configurations, and returns the app instance.
    
    Returns:
        Flask: The configured Flask app instance.
    """
    return app
