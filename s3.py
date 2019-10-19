import logging
import boto3
from botocore.exceptions import ClientError
import tempfile

BUCKET_NAME='search-in-video'
s3_client = boto3.client('s3')

def upload(file_obj, object_name, bucket=BUCKET_NAME):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :return: True if file was uploaded, else False
    """
    # Upload the file
    try:
        response = s3_client.upload_fileobj(file_obj, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def uploadfile(filename, objname, bucket=BUCKET_NAME):
    try:
        response = s3_client.upload_file(filename, bucket, objname)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def download(filename):
    f = tempfile.TemporaryFile()
    try:
        s3_client.download_fileobj(BUCKET_NAME, filename, f)
        f.seek(0)
        return f.read().decode()
    except ClientError as e:
        logging.error(e)
        return False

def delete(filename, bucket=BUCKET_NAME):
    try:
        s3_client.delete_object(bucket, filename)
    except ClientError as e:
        logging.error(e)
        return False
    return True
