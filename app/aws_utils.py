# app/aws_utils.py
import boto3
from flask import current_app

def upload_file_to_s3(file, bucket_name, acl="public-read"):
    s3 = boto3.client('s3')
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        print("Something Happened: ", e)
        return e

    return f"{current_app.config['S3_LOCATION']}{file.filename}"
