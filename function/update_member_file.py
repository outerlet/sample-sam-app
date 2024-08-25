import json
import boto3
from data.member import Member

S3_BUCKET_NAME = 'sample-app-bucket'
S3_FILE_NAME = 'member.csv'
TEMP_FILE_NAME = 'member_tmp.csv'
TEMP_FILE_PATH = f'/tmp/{TEMP_FILE_NAME}'


def lambda_handler(event, context):
    print(f'event = {event}')

    records = [Member(record['dynamodb']['NewImage']) for record in event['Records']]

    s3_client = boto3.client('s3')

    try:
        s3_client.download_file(
            Bucket=S3_BUCKET_NAME,
            Key=S3_FILE_NAME,
            Filename=TEMP_FILE_PATH,
        )
    except Exception as e:
        print(f'Download Error: {e}')

    with open(TEMP_FILE_PATH, 'a') as f:
        for record in records:
            f.write(f'{record}\n')

    s3_client.upload_file(
        Filename=TEMP_FILE_PATH,
        Bucket=S3_BUCKET_NAME,
        Key=S3_FILE_NAME,
    )

    return json.dumps({
        "status_code": 200,
    })
