
import requests
import logging
from typing import Optional
from abc import ABC

from app.utils.exceptions import(
    ServiceError,
    ServiceTimeoutError,
    ServiceUnavailableError

)

class BaseService(ABC):
  
    def __init__(self, service_name: str, base_url: str, default_timeout: int = 30):
        
        self.service_name = service_name
        self.base_url = base_url.rstrip('/')
        self.default_timeout = default_timeout
        self.logger = logging.getLogger(f"{__name__}.{service_name}")
    
    def _build_url(self, endpoint: str) -> str:
        """Construye URL completa"""
        endpoint = endpoint.lstrip('/')
        return f"{self.base_url}/{endpoint}"
    
    def _log_request(self, method: str, url: str, **kwargs):
        """Log de request saliente"""
        self.logger.info(f"→ {method} {url}")
        if 'json' in kwargs:
            self.logger.debug(f"  Request body: {kwargs['json']}")
    
    def _log_response(self, response: requests.Response):
        """Log de response recibida"""
        self.logger.info(
            f"← {response.status_code} from {self.service_name} "
            f"({response.elapsed.total_seconds():.2f}s)"
        )
    
    def request(
        self,
        method: str,
        endpoint: str,
        timeout: Optional[int] = None,
        **kwargs
    ) -> requests.Response:
      
        url = self._build_url(endpoint)
        timeout = timeout or self.default_timeout
        
       
        default_headers = {
            'Content-Type': 'application/json',
            'User-Agent': f'MLSToolbox-Server/{self.service_name}',
        }
        
       
        headers = kwargs.pop('headers', {})
        headers = {**default_headers, **headers}
        
        self._log_request(method, url, **kwargs)
        
        try:
            response = requests.request(
                method=method,
                url=url,
                timeout=timeout,
                headers=headers,
                **kwargs
            )
            
            self._log_response(response)
            
            
            response.raise_for_status()
            
            return response
            
        except requests.exceptions.Timeout:
            self.logger.error(f"Timeout calling {self.service_name} after {timeout}s")
            raise ServiceTimeoutError(self.service_name, timeout)
        
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"Connection error to {self.service_name}: {str(e)}")
            raise ServiceUnavailableError(self.service_name, str(e))
        
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP error from {self.service_name}: {str(e)}")
            raise ServiceError(
                self.service_name,
                response.status_code,
                response.text[:200]  
            )
        
        except Exception as e:
            self.logger.exception(f"Unexpected error calling {self.service_name}")
            raise ServiceUnavailableError(self.service_name, str(e))
    
    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """Wrapper para GET request"""
        return self.request('GET', endpoint, **kwargs)
    
    def post(self, endpoint: str, **kwargs) -> requests.Response:
    
        return self.request('POST', endpoint, **kwargs)
    
    def health_check(self) -> bool:
        
        try:
            response = self.get('/', timeout=5)
            return response.ok
        except Exception:
            return False