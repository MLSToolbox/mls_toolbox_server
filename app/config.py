import os

class Config:
    """Configuración del gateway."""
    
    SERVICES = {
        "code_generator": os.getenv('CODE_GENERATOR_URL', 'http://mls_code_generator:5050'),
        "code_assessment": os.getenv('CODE_ASSESSMENT_URL', 'http://mls_toolbox_code_assessment:5060'),
    }
    
    ROUTES = {
        "/api/create_app": "code_generator",
        "/api/test_create_app": "code_generator",
        "/api/get_config": "code_generator",
        "/api/get_base_editor": "code_generator",
        "/api/get_editor": "code_generator",
        "/api/get_available_editor": "code_generator",
        "/api/upload": "code_assessment",
        "/api/analyze/<uuid>": "code_assessment",
    }
    
    # Configuración del servidor (desde variables de entorno)
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', '5000'))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

