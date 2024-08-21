from dataclasses import dataclass
from enum import Enum
import json
import boto3

S3_BUCKET_NAME = 'test-data'
S3_FILE_NAME = 'member.csv'
TEMP_FILE_NAME = 'member_tmp.csv'
TEMP_FILE_PATH = f'/tmp/{TEMP_FILE_NAME}'


class Sex(Enum):
    MALE = 0
    FEMALE = 1


@dataclass
class Member:
    seq: int
    name: str
    age: int
    sex: Sex

    def __init__(self, record: dict):
        self.seq = int(record['seq']['N'])
        self.name = record['name']['S']
        self.age = int(record['age']['N'])

        sex = record['sex']['S']
        if sex == Sex.MALE.name:
            self.sex = Sex.MALE
        elif sex == Sex.FEMALE.name:
            self.sex = Sex.FEMALE
        else:
            raise ValueError('sex value must be MALE or FEMALE')

    def __str__(self):
        return f'{self.seq},{self.name},{self.age},{self.sex.name}'


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
