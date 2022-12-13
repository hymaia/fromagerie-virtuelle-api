import json
import logging
import os
import zipfile
from io import BytesIO

import boto3

logging.basicConfig()

s3 = boto3.client('s3')

BUCKET_NAME = os.environ["BUCKET_NAME"]


def get_last_year_data(event, context):
    presign_url = s3.generate_presigned_url('get_object',
                                            Params={'Bucket': BUCKET_NAME,
                                                    'Key': 'test.json',
                                                    'ResponseContentType': 'application/json'})

    response = {
        'statusCode': 308,
        'headers': {
            'Location': presign_url,
        },
    }
    return response
    #return create_zip_file_stream(BUCKET_NAME, 'commands/month=JANUARY')


def create_zip_file_stream(bucket_name, bucket_file_path):
    files_collection = s3.list_objects(Bucket=bucket_name, Prefix=bucket_file_path)["Contents"]
    files = list(map(lambda x: x["Key"], files_collection))
    archive = BytesIO()

    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as zip_archive:
        for file in files:
            with zip_archive.open(file, 'w') as file1:
                data = s3.get_object(Bucket=bucket_name, Key=file)
                file1.write(data['Body'].read())
    return archive
