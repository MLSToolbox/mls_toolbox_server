from app.utils.exceptions.mls_toolbox_exception import MLSToolboxException

class ServiceUnavailableError(MLSToolboxException):
    status_code = 503

    def __init__(self, service_name: str, details: str = None):
        message = f"Service '{service_name}' is unavailable"
        if details:
            message += f": {details}"
        super().__init__(message, payload={'service': service_name})