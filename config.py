import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DROPZONE_UPLOAD_MULTIPLE = False  # Allow only single file upload
    DROPZONE_ALLOWED_FILE_TYPE = 'image'
    DROPZONE_MAX_FILE_SIZE = 3  # MB

    # AWS S3 configuration
    S3_BUCKET = os.getenv('S3_BUCKET')
    AWS_REGION = os.getenv('AWS_REGION', 'ap-southeast-2')  # Default to ap-southeast-2 if not set
    S3_LOCATION = f'https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/'

    # Additional AWS keys for boto3
    AWS_ACCESS_KEY_ID = os.getenv('S3_KEY')
    AWS_SECRET_ACCESS_KEY = os.getenv('S3_SECRET')
