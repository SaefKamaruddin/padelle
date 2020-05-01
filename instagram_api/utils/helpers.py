import boto3
import botocore
import os
from app import app

s3 = boto3.client(
    "s3",
    aws_access_key_id=app.config.get('AWS_KEY'),
    aws_secret_access_key=app.config.get('AWS_SECRET')
)


def upload_file_to_aws(file):
    try:
        s3.upload_fileobj(
            file,
            app.config.get('AWS_BUCKET'),
            file.filename,
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": file.content_type
            }
        )
        return file.filename

    except Exception as e:
        print("Something happened", e)
        return e
