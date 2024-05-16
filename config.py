import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://user:password@hostname:port/dbname')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DROPZONE_UPLOAD_MULTIPLE = False  # Allow only single file upload
    DROPZONE_ALLOWED_FILE_TYPE = 'image'
    DROPZONE_MAX_FILE_SIZE = 3  # MB

    # AWS S3 configuration
    S3_BUCKET = os.getenv('S3_BUCKET')
    S3_LOCATION = f'https://{S3_BUCKET}.s3.amazonaws.com/'

    # AWS region
    AWS_REGION = os.getenv('AWS_REGION', 'ap-southeast-2')  # Default to ap-southeast-2 if not set
