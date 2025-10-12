
import os
from app import create_app
from waitress import serve


def main():
   
    
    env = os.getenv('FLASK_ENV', 'development')
    execution_mode = os.getenv('EXECUTION_MODE', 'debug')
    
    
    app = create_app(env)
    
    
    host = app.config['HOST']
    port = app.config['PORT']
    
    if execution_mode == 'prod':
        
        app.logger.info(f"Starting Waitress server on {host}:{port}")
        serve(app, host=host, port=port, threads=4)
    else:
        
        app.logger.info(f"Starting Flask development server on {host}:{port}")
        app.run(host=host, port=port, debug=app.config['DEBUG'])


if __name__ == '__main__':
    main()