

from typing import Dict, Any
from flask import current_app

from app.services.base_service import BaseService


class CodeGeneratorService(BaseService):
   
    
    def __init__(self):
        config = current_app.config
        super().__init__(
            service_name='CodeGenerator',
            base_url=config['CODE_GENERATOR_BASE_URL'],
            default_timeout=config['GENERATION_TIMEOUT']
        )
    
    def create_app(self, code: Dict[str, Any], nodes: Dict[str, Any]) -> bytes:
        
        payload = {
            'code': code,
            'nodes': nodes
        }
        
        response = self.post('/api/create_app', json=payload)
        return response.content
    
    def get_config(self) -> Dict[str, Any]:
       
        response = self.get('/api/get_config')
        return response.json()
    
    def get_base_editor(self) -> Dict[str, Any]:
      
        response = self.get('/api/get_base_editor')
        return response.json()
    
    def get_editor(self, template_name: str) -> Dict[str, Any]:
        
        response = self.post('/api/get_editor', data=template_name.encode())
        return response.json()
    
    def get_available_editors(self) -> Dict[str, Any]:
        
        response = self.get('/api/get_available_editor')
        return response.json()