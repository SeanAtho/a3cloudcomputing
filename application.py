from flask import Flask
from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Environment variables for configuration
    DEBUG = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    HOST = os.environ.get('FLASK_HOST', '127.0.0.1')
    PORT = int(os.environ.get('FLASK_PORT', 5000))
    
    app.run(debug=DEBUG, host=HOST, port=PORT)
