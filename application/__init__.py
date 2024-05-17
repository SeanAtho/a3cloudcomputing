from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_dropzone import Dropzone
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
dropzone = Dropzone()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    dropzone.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from . import routes, models
        db.create_all()

        # Register blueprints
        from .routes import main as main_blueprint
        app.register_blueprint(main_blueprint)

    return app
