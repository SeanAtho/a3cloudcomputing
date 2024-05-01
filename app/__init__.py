from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_dance.contrib.google import make_google_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Set a secret key for security purposes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'  # Configure your database URI

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'google.login'  # Redirect to Google login if authentication is required

# Setup Google OAuth
app.config['GOOGLE_OAUTH_CLIENT_ID'] = 'your_google_client_id_here'
app.config['GOOGLE_OAUTH_CLIENT_SECRET'] = 'your_google_client_secret_here'
google_bp = make_google_blueprint(scope=["profile", "email"], redirect_to='after_login')  # Define the endpoint to redirect after login
app.register_blueprint(google_bp, url_prefix="/login")

# Import models to ensure they are known to Flask-Migrate
from app import models

# Flask-Login configuration
@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))

# Routes need to be imported after initializing components to avoid circular imports
from app import routes
