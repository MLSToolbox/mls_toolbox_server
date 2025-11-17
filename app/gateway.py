import json

import requests
from flask import Request, Response

from config import Config


class Gateway:
    """Gateway que solo reenvía peticiones."""
    
    def __init__(self):
        """Inicializa el gateway."""
        self.services = Config.SERVICES
        self.routes = Config.ROUTES
    
    def forward_request(self, request: Request, service_name: str) -> Response:
        """
        Reenvía la petición exactamente como llega.
        
        Args:
            request: Petición Flask recibida
            service_name: Nombre del servicio destino
            
        Returns:
            Respuesta del servicio destino
        """
        base_url = self.services[service_name]
        target_url = f"{base_url}{request.path}"
        
        if request.query_string:
            target_url += f"?{request.query_string.decode('utf-8')}"
        
        try:
            response = requests.request(
                method=request.method,
                url=target_url,
                headers={key: value for key, value in request.headers if key != 'Host'},
                data=request.get_data(),
                cookies=request.cookies,
                allow_redirects=False,
                timeout=300
            )
            
            # Filter out CORS headers from backend to avoid duplication
            # The gateway's CORS configuration will handle these
            excluded_headers = [
                'Access-Control-Allow-Origin',
                'Access-Control-Allow-Methods',
                'Access-Control-Allow-Headers',
                'Access-Control-Allow-Credentials',
                'Access-Control-Expose-Headers',
                'Access-Control-Max-Age'
            ]
            
            response_headers = {
                key: value for key, value in response.headers.items()
                if key not in excluded_headers
            }
            
            return Response(
                response.content,
                status=response.status_code,
                headers=response_headers
            )
            
        except requests.exceptions.RequestException as e:
            return Response(
                json.dumps({"error": str(e)}),
                status=503,
                mimetype='application/json'
            )
    
    def get_service(self, path: str) -> str:
        """
        Obtiene el servicio que maneja una ruta.
        Soporta rutas con parámetros como /api/analyze/<uuid>
        
        Args:
            path: Ruta de la petición
            
        Returns:
            Nombre del servicio o None
        """
        if path in self.routes:
            return self.routes[path]
        
        for route_pattern, service in self.routes.items():
            if self._match_route(route_pattern, path):
                return service
        
        return None
    
    def _match_route(self, pattern: str, path: str) -> bool:
        """
        Verifica si un path coincide con un patrón de ruta.
        
        Args:
            pattern: Patrón de ruta (ej: /api/analyze/<uuid>)
            path: Ruta real (ej: /api/analyze/abc-123)
            
        Returns:
            True si coincide, False si no
        """
        pattern_parts = pattern.split('/')
        path_parts = path.split('/')
        
        if len(pattern_parts) != len(path_parts):
            return False
        
        for pattern_part, path_part in zip(pattern_parts, path_parts):
            if pattern_part.startswith('<') and pattern_part.endswith('>'):
                continue
            if pattern_part != path_part:
                return False
        
        return True

