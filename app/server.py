from flask import Flask, request
from flask_cors import CORS, cross_origin
from waitress import serve

from gateway import Gateway
from config import Config

app = Flask(__name__)
gateway = Gateway()


def proxy_handler():
    """Handler único que reenvía todas las peticiones."""
    service = gateway.get_service(request.path)
    if not service:
        return {"error": "Route not configured"}, 404
    return gateway.forward_request(request, service)


for route_path in Config.ROUTES.keys():
    app.add_url_rule(
        route_path,
        endpoint=route_path,
        view_func=cross_origin()(proxy_handler),
        methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS']
    )


@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def home():
    """Endpoint de verificación del gateway."""
    return 'hello from mls_toolbox_server'


if __name__ == '__main__':
    CORS(app, supports_credentials=True, origins=['*'])
    app.config["CORS_HEADERS"] = ["Content-Type", "X-Requested-With", "X-CSRFToken"]
    
    if Config.DEBUG:
        app.run(host=Config.HOST, port=Config.PORT, debug=True)
    else:
        serve(app, host=Config.HOST, port=Config.PORT)

