class MLSToolboxException(Exception):
    
    status_code = 500
    
    def __init__(self, message: str, status_code: int = None, payload: dict = None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        
        rv = dict(self.payload or ())
        rv['error'] = self.message
        rv['status_code'] = self.status_code
        return rv