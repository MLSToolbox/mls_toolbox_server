

import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask

from app.config import get_config
from app.extensions import init_extensions
from app.routes import register_blueprints
from app.middleware.error_handler import register_error_handlers
from app.middleware import logging_middleware


def create_app(config_name: str = None) -> Flask:
    
    app = Flask(__name__)
    
    
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    
    
    setup_logging(app)
    
    
    init_extensions(app)
    
    
    register_blueprints(app)
    
    
    register_error_handlers(app)
    
    
    app.before_request(logging_middleware.before_request)
    app.after_request(logging_middleware.after_request)
    
   
    if hasattr(config_class, 'init_app'):
        config_class.init_app(app)
    
    app.logger.info(f"Application created with config: {config_name}")
    
    return app


def setup_logging(app: Flask):
    """
    Configura el sistema de logging de la aplicación.
    
    Args:
        app: Instancia de Flask
    """
   
    log_dir = os.path.dirname(app.config['LOG_FILE'])
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    
    log_level = getattr(logging, app.config['LOG_LEVEL'].upper())
    
    
    file_handler = RotatingFileHandler(
        app.config['LOG_FILE'],
        maxBytes=app.config['LOG_MAX_BYTES'],
        backupCount=app.config['LOG_BACKUP_COUNT']
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter(app.config['LOG_FORMAT']))
    
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter(app.config['LOG_FORMAT']))
    
    
    app.logger.setLevel(log_level)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    
    
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)