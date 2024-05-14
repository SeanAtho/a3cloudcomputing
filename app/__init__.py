from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_dropzone import Dropzone  # Import Dropzone if you decide to use it

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
dropzone = Dropzone()  # Initialize Dropzone

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)  # Load configuration from config class

    # Initialize extensions with the app instance
    db.init_app(app)
    migrate.init_app(app, db)  # Set up Flask-Migrate with the app and db
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'  # Redirect to login page for unauthorized users
    login_manager.login_message = "Please log in to access this page."

    # Configure Dropzone for file uploads if using Dropzone
    app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
    app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
    app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
    app.config['DROPZONE_MAX_FILE_SIZE'] = 3
    app.config['DROPZONE_PARALLEL_UPLOADS'] = 3
    dropzone.init_app(app)

    # Register blueprints for application routing
    from .routes import main as main_routes
    app.register_blueprint(main_routes)

    # Global error handlers for common HTTP errors
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()  # Rollback db transactions on internal errors
        return render_template('500.html'), 500

    return app
