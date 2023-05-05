import os
import gzip
import json

import boto3


def is_gzip(file_content):
    """
    Check if the file is compressed in Gzip format.
    :param file_content:
    :return:
    """
    return file_content[:2] == b'\x1f\x8b'


def token_from_s3_bucket():
    s3 = boto3.client('s3')
    # read the file
    obj = s3.get_object(Bucket=os.environ.get('BUCKET_NAME'), Key=os.environ.get('FILE_NAME'))
    file_content = obj['Body'].read()

    # Check if the file is compressed in Gzip format
    if is_gzip(file_content):
        # If the file is compressed in Gzip format, decompress it
        file_content = gzip.decompress(file_content)

    # Decode the file content as utf-8
    decoded_content = file_content.decode('utf-8')
    token = json.loads(decoded_content.strip())
    return token


def token_to_s3_bucket(data):
    s3 = boto3.client('s3')
    # upload the file
    s3.put_object(Body=json.dumps(data), Bucket=os.environ.get('BUCKET_NAME'), Key=os.environ.get('FILE_NAME'))


def token_from_local_file():
    with open(os.environ.get('FILE_NAME'), 'r') as f:
        token = json.loads(f.read())
    return token


def token_to_local_file(data):
    with open(os.environ.get('FILE_NAME'), 'w') as f:
        f.write(json.dumps(data))
