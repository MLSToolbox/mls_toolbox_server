
from app.utils.exceptions.mls_toolbox_exception import MLSToolboxException


class ServiceError(MLSToolboxException):
  
    
    def __init__(self, service_name: str, status_code: int, details: str = None):
        message = f"Service '{service_name}' returned error {status_code}"
        if details:
            message += f": {details}"
        super().__init__(message, status_code=status_code, payload={'service': service_name})