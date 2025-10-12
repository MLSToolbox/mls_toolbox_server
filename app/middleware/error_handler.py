
import logging
from flask import jsonify
from werkzeug.exceptions import HTTPException

from app.utils.exceptions import MLSToolboxException

logger = logging.getLogger(__name__)


def handle_mls_exception(error: MLSToolboxException):
    
    logger.error(f"{error.__class__.__name__}: {error.message}")
    
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def handle_http_exception(error: HTTPException):
   
    logger.warning(f"HTTP {error.code}: {error.description}")
    
    response = jsonify({
        'error': error.description,
        'status_code': error.code
    })
    response.status_code = error.code
    return response


def handle_generic_exception(error: Exception):
    
    logger.exception("Unhandled exception:")
    
    response = jsonify({
        'error': 'Internal server error',
        'status_code': 500
    })
    response.status_code = 500
    return response


def register_error_handlers(app):
    app.register_error_handler(MLSToolboxException, handle_mls_exception)
    app.register_error_handler(HTTPException, handle_http_exception)
    app.register_error_handler(Exception, handle_generic_exception)