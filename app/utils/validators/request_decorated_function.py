

from functools import wraps
from flask import request

from app.utils.exceptions import BadRequestError


def require_json(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            raise BadRequestError('Content-Type must be application/json')
        
        if not request.json:
            raise BadRequestError('Request body cannot be empty')
        
        return f(*args, **kwargs)
    
    return decorated_function


def require_fields(*fields):
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.json
            
            missing_fields = [field for field in fields if field not in data]
            
            if missing_fields:
                raise BadRequestError(
                    f"Missing required fields: {', '.join(missing_fields)}"
                )
            
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator


def require_binary_data(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.data:
            raise BadRequestError('Request body cannot be empty')
        
        return f(*args, **kwargs)
    
    return decorated_function