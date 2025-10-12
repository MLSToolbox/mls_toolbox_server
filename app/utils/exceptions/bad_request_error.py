
from app.utils.exceptions.mls_toolbox_exception import MLSToolboxException


class BadRequestError(MLSToolboxException):
    
    status_code = 400
    

