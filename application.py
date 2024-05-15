import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    DEBUG = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    HOST = os.environ.get('FLASK_HOST', '0.0.0.0')  # Changed to 0.0.0.0 to be accessible externally
    PORT = int(os.environ.get('FLASK_PORT', 5000))
    
    app.run(debug=DEBUG, host=HOST, port=PORT)
