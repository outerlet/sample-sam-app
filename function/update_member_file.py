import json
import boto3
from data.member import Member
from awsservice.s3 import try_download_s3_file, upload_s3_file

S3_BUCKET_NAME = 'sample-app-bucket'
S3_FILE_NAME = 'members.csv'
TEMP_FILE_NAME = 'members_temp.csv'
TEMP_FILE_PATH = f'/tmp/{TEMP_FILE_NAME}'


def lambda_handler(event, context):
    print(f'event = {event}')

    members = [Member(record['dynamodb']['NewImage']) for record in event['Records']]

    s3_client = boto3.client('s3')

    try_download_s3_file(
        s3_client=s3_client,
        bucket_name=S3_BUCKET_NAME,
        file_name=S3_FILE_NAME,
        download_filepath=TEMP_FILE_PATH,
    )

    with open(TEMP_FILE_PATH, 'a') as f:
        for member in members:
            f.write(f'{member}\n')

    success_upload = upload_s3_file(
        s3_client=s3_client,
        local_filepath=TEMP_FILE_PATH,
        bucket_name=S3_BUCKET_NAME,
        file_name=S3_FILE_NAME,
    )

    if not success_upload:
        return json.dumps({
            'status_code': 400,
            'message': 'Failed: Upload to S3'
        })

    return json.dumps({
        "status_code": 200,
    })
