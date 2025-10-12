
from flask import current_app

from app.services.base_service import BaseService


class CodeAssessorService(BaseService):
    
    def __init__(self):
        config = current_app.config
        super().__init__(
            service_name='CodeAssessor',
            base_url=config['CODE_ASSESSOR_BASE_URL'],
            default_timeout=config['ASSESSMENT_TIMEOUT']
        )
    
    def rate_app(self, code_zip: bytes) -> bytes:
       
        headers = {'Content-Type': 'application/x-binary'}
        
        response = self.post(
            '/api/rate_app',
            data=code_zip,
            headers=headers
        )
        
        return response.content
    
    def get_report(self, code_zip: bytes, query_params: str = '') -> bytes:
       
        headers = {'Content-Type': 'application/x-binary'}
        endpoint = f'/api/get_report?{query_params}' if query_params else '/api/get_report'
        
        response = self.post(
            endpoint,
            data=code_zip,
            headers=headers
        )
        
        return response.content