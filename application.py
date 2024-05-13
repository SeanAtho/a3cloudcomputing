from flask import Flask
from a3cloudcomputing.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialize the Flask application
application = Flask(__name__)
application.config.from_object(Config)

# Initialize database with SQLAlchemy
db = SQLAlchemy(application)

# Setup Flask-Migrate for database migrations
migrate = Migrate(application, db)

# Initialize Flask-Login
login_manager = LoginManager(application)
login_manager.login_view = 'login'  # Specifies the login view

# Import routes and models to register them with the Flask application
from app import routes, models

if __name__ == '__main__':
    application.run(debug=True)  # Only for local development
