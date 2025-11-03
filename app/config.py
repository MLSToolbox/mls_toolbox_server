

class Config:
    """Configuración del gateway."""
    
    SERVICES = {
        "code_generator": "http://localhost:5050",
        "code_assessment": "http://localhost:5060",
    }
    
    ROUTES = {
        "/api/create_app": "code_generator",
        "/api/test_create_app": "code_generator",
        "/api/get_config": "code_generator",
        "/api/get_base_editor": "code_generator",
        "/api/get_editor": "code_generator",
        "/api/get_available_editor": "code_generator",
        "/api/upload-zip": "code_assessment",
        "/api/analyze": "code_assessment",
    }
    
    HOST = "0.0.0.0"
    PORT = 5000
    DEBUG = False

