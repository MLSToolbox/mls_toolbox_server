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
            
            return Response(
                response.content,
                status=response.status_code,
                headers=dict(response.headers)
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
        
        Args:
            path: Ruta de la petición
            
        Returns:
            Nombre del servicio o None
        """
        return self.routes.get(path)

