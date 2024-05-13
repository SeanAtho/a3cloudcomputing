from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import DevelopmentConfig

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    login_manager.init_app(app)

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
