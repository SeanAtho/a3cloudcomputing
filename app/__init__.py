from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_dance.contrib.google import make_google_blueprint
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Database setup
db = SQLAlchemy(app)

# Login manager setup
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Google OAuth setup
google_bp = make_google_blueprint(client_id="your-google-client-id",
                                  client_secret="your-google-client-secret",
                                  scope=["profile", "email"],
                                  redirect_to='google_login')
app.register_blueprint(google_bp, url_prefix="/login")

from app import routes, models
