import boto3
import botocore
import os

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ.get('AWS_KEY'),
    aws_secret_access_key=os.environ.get('AWS_SECRET')
)


def upload_file_to_aws(file):
    try:
        s3.upload_fileobj(
            file,
            os.environ.get('BUCKET_NAME'),
            file.filename,
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": file.content_type
            }
        )
        return file.filename

    except AttributeError as e:
        print("Something happened", e)
        return e
