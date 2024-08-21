from dataclasses import dataclass
from enum import Enum
import json
import boto3


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
        return f'seq = {self.seq}, name = {self.name}, age = {self.age}, sex = {self.sex.name}'


def lambda_handler(event, context):
    print(f'event = {event}')

    records = [Member(record['dynamodb']['NewImage']) for record in event['Records']]

    for record in records:
        print(f'New Record: {record}')

    return json.dumps({
        "status_code": 200,
    })
