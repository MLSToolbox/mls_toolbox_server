

from flask_cors import CORS


cors = CORS()


def init_extensions(app):
    """Inicializa todas las extensiones con la app"""
    cors.init_app(
        app,
        resources={
            r"/api/*": {
                "origins": app.config['CORS_ORIGINS'],
                "methods": app.config['CORS_METHODS'],
                "allow_headers": app.config['CORS_ALLOW_HEADERS']
            }
        }
    )