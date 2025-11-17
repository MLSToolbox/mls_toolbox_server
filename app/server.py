from flask import Flask, request
from flask_cors import CORS
from waitress import serve

from gateway import Gateway
from config import Config

app = Flask(__name__)

# Configure CORS once globally - do NOT use @cross_origin decorator
CORS(app, 
     resources={r"/*": {"origins": "*"}},
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
     supports_credentials=False)

gateway = Gateway()


def proxy_handler(**kwargs):
    """Handler único que reenvía todas las peticiones."""
    service = gateway.get_service(request.path)
    if not service:
        return {"error": "Route not configured"}, 404
    return gateway.forward_request(request, service)


for route_path in Config.ROUTES.keys():
    app.add_url_rule(
        route_path,
        endpoint=route_path,
        view_func=proxy_handler,  # Removed @cross_origin() decorator
        methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS']
    )


@app.route('/', methods=['GET', 'POST'])
def home():
    """Endpoint de verificación del gateway."""
    return 'hello from mls_toolbox_server'


if __name__ == '__main__':
    if Config.DEBUG:
        app.run(host=Config.HOST, port=Config.PORT, debug=True)
    else:
        serve(app, host=Config.HOST, port=Config.PORT)

