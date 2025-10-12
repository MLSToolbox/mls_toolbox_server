

import os
from typing import List


class Config:
   
    
   
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:4200').split(',')
    CORS_METHODS = ['GET', 'POST', 'OPTIONS']
    CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization', 'X-Requested-With']
    
    
    CODE_GENERATOR_HOST = os.getenv('MLS_CODE_GENERATOR_URI', 'localhost')
    CODE_GENERATOR_PORT = os.getenv('MLS_CODE_GENERATOR_PORT', '5050')
    CODE_GENERATOR_BASE_URL = f"http://{CODE_GENERATOR_HOST}:{CODE_GENERATOR_PORT}"
    
   
    CODE_ASSESSOR_HOST = os.getenv('MLS_CODE_ASSESS_URI', 'localhost')
    CODE_ASSESSOR_PORT = os.getenv('MLS_CODE_ASSESS_PORT', '5060')
    CODE_ASSESSOR_BASE_URL = f"http://{CODE_ASSESSOR_HOST}:{CODE_ASSESSOR_PORT}"
    
    
    DEFAULT_TIMEOUT = 30
    GENERATION_TIMEOUT = 60
    ASSESSMENT_TIMEOUT = 300
    
    
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = 'logs/server.log'
    LOG_MAX_BYTES = 10 * 1024 * 1024  
    LOG_BACKUP_COUNT = 5
    
    
    HOST = '0.0.0.0'
    PORT = int(os.getenv('PORT', '5000'))
    DEBUG = False


class DevelopmentConfig(Config):
    
    DEBUG = True
    LOG_LEVEL = 'DEBUG'


class TestingConfig(Config):
   
    TESTING = True
    CODE_GENERATOR_BASE_URL = 'http://mock-generator:5050'
    CODE_ASSESSOR_BASE_URL = 'http://mock-assessor:5060'


class ProductionConfig(Config):
   
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    
   
   




config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(env: str = None) -> Config:

    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    
    return config.get(env, config['default'])