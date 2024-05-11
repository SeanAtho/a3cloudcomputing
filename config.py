import os
import boto3
import json
from dotenv import load_dotenv

# Load environment variables from a .env file for local development
load_dotenv()

# Create a Secrets Manager client
session = boto3.session.Session()
client = session.client(
    service_name='secretsmanager',
    region_name=os.getenv('AWS_REGION', 'us-west-2')  # Default to us-west-2 if not set in .env
)

def get_secret(secret_name):
    """Retrieve secrets from AWS Secrets Manager"""
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)
    except Exception as e:
        print(f"Error retrieving secret {secret_name}: {str(e)}")
        return None

# Retrieve secrets
db_credentials = get_secret('my_database_credentials')
email_credentials = get_secret('my_email_credentials')
google_credentials = get_secret('my_google_oauth_credentials')

class Config:
    """Base configuration"""
    SECRET_KEY = db_credentials.get('SECRET_KEY') if db_credentials else os.environ.get('SECRET_KEY', 'you-will-never-guess')
    SQLALCHEMY_DATABASE_URI = db_credentials.get('DATABASE_URI') if db_credentials else os.environ.get('DATABASE_URL', 'sqlite:///yourdatabase.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Google OAuth
    GOOGLE_CLIENT_ID = google_credentials.get('GOOGLE_CLIENT_ID') if google_credentials else os.environ.get('GOOGLE_CLIENT_ID', 'your-google-client-id')
    GOOGLE_CLIENT_SECRET = google_credentials.get('GOOGLE_CLIENT_SECRET') if google_credentials else os.environ.get('GOOGLE_CLIENT_SECRET', 'your-google-client-secret')
    
    # Email configuration for AWS SES
    MAIL_SERVER = 'email-smtp.us-west-2.amazonaws.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = email_credentials.get('USERNAME') if email_credentials else os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = email_credentials.get('PASSWORD') if email_credentials else os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-admin-email@example.com']

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
