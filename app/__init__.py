from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
photos = UploadSet('photos', IMAGES)

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'  # Specify the login view
    login_manager.login_message = "Please log in to access this page."

    # Configure image uploads
    app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'  # Local folder for testing; change to S3 bucket in production
    configure_uploads(app, photos)
    patch_request_class(app)  # Optional: limit the size of uploads

    # Migrate setup
    migrate = Migrate(app, db)

    # Register blueprints
    from .routes import main as main_routes
    app.register_blueprint(main_routes)

    return app
