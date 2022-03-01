import boto3
import boto3.s3
from botocore.exceptions import ClientError
import os

ost = []

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        print(e)
        return False
    return True


s3 = boto3.client('s3',
                  aws_access_key_id='AKIA2O4I5LAERPDCRDAK',
                  aws_secret_access_key='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')

with open("Dockerfile", "rb") as f:
    s3.upload_fileobj(f, 'creo-hrm-dev', 'Dockerfile')