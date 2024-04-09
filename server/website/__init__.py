from flask import Flask
from importlib import import_module
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth_blueprint.login' 
migrate = Migrate()
seeder = FlaskSeeder()

def register_extensions(app):
    app.app_context().push()
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    seeder.init_app(app, db)

def register_blueprints(app):
    for module_name in ('settings','home','auth'):
        module = import_module('website.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def create_app(config):
    app = Flask(__name__)
    app.static_folder = 'static'
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    return app