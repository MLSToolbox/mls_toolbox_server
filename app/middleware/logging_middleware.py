

import time
import logging
from flask import request, g

logger = logging.getLogger(__name__)


def before_request():
    
    g.start_time = time.time()
    
    logger.info(
        f"→ {request.method} {request.path} "
        f"from {request.remote_addr}"
    )
    
    if request.json:
        logger.debug(f"  Request body: {request.json}")


def after_request(response):
    
    if hasattr(g, 'start_time'):
        elapsed = time.time() - g.start_time
        logger.info(
            f"← {response.status_code} {request.method} {request.path} "
            f"({elapsed:.3f}s)"
        )
    
    return response
