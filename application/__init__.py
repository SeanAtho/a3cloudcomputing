from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_dropzone import Dropzone

db = SQLAlchemy()
login_manager = LoginManager()
dropzone = Dropzone()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    login_manager.init_app(app)
    dropzone.init_app(app)
    
    with app.app_context():
        from . import routes
        db.create_all()
    
    return app
