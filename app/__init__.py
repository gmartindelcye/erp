# app 
from flask import Flask
from werkzeug.exceptions import default_exceptions

from app.helpers.handler.handler_errors import HandlerErrors
from app.middleware.middleware import Middleware
from app.models import db
from .config.config import config
from flask_migrate import Migrate


def create_app(config_type = 'LOCALDB'):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(config[config_type])
    db.init_app(app)
    migrate = Migrate(app, db)
    app.wsgi_app = Middleware(app)
    for exception in default_exceptions:
        app.register_error_handler(exception, HandlerErrors.handler_http_error)
    return app


