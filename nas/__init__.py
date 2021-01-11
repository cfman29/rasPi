from flask import Flask, Blueprint
from nas.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)

    from nas.primary.routes import primary
    app.register_blueprint(primary)
    from nas.users.routes import users
    app.register_blueprint(users)
    return app