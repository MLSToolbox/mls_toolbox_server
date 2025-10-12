
from app.utils.exceptions.mls_toolbox_exception import MLSToolboxException
class ServiceTimeoutError(MLSToolboxException):
    """Error cuando un servicio downstream hace timeout"""
    status_code = 504
    
    def __init__(self, service_name: str, timeout: int):
        message = f"Service '{service_name}' timed out after {timeout}s"
        super().__init__(message, payload={'service': service_name, 'timeout': timeout})