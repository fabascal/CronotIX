import os
from flask import Flask, g, after_this_request
from importlib import import_module
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
# Configuración para log
import logging
import re
from logging.handlers import TimedRotatingFileHandler

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth_blueprint.login' 
migrate = Migrate()
seeder = FlaskSeeder()
csrf = CSRFProtect()

def generate_nonce():
    return os.urandom(16).hex()

def register_extensions(app):
    app.app_context().push()
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    seeder.init_app(app, db)
    csrf.init_app(app)

def register_blueprints(app):
    for module_name in ('settings','home','auth'):
        module = import_module('website.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)
        
def configure_logging():
    # Crear el directorio de logs si no existe
    if not os.path.exists('log'):
        os.makedirs('log')

    # Configurar el archivo de log con rotación cada 7 días
    log_file = 'log/cronotix.log'
    handler = TimedRotatingFileHandler(log_file, when="D", interval=7, backupCount=4)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    handler.setFormatter(formatter)

    # Configurar el nivel del manejador
    handler.setLevel(logging.INFO)  # Cambia esto según tus necesidades (DEBUG, WARNING, ERROR, etc.)

    # Añadir el manejador al logger raíz
    logging.getLogger().setLevel(logging.INFO)
    logging.getLogger().addHandler(handler)

def create_app(config):
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    #CORS(app, resources={r"/api/*": {"origins": ["https://tu-frontend.com", "http://localhost:3000"]}})
    app.static_folder = 'static'
    app.config.from_object(config)
    configure_logging()
    # @app.before_request
    # def before_request():
    #     g.nonce = generate_nonce()
    # @app.after_request
    # def add_security_headers(response):
    #     csp = f"script-src 'self' 'nonce-{g.nonce}'; object-src 'none';"
    #     response.headers['Content-Security-Policy'] = csp
    #     return response
    app.jinja_env.add_extension('jinja2.ext.do')
    register_extensions(app)
    register_blueprints(app)
    return app