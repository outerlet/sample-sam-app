from typing import Optional
from dataclasses import dataclass
import json
import boto3

TABLE_NAME = 'UserMessage'


@dataclass
class UserMessage:
    sender: str
    receiver: str
    message: str

    def __init__(self, event: dict):
        self.sender = event['sender']
        self.receiver = event['receiver']
        self.message = event['message']

    def __str__(self):
        return f'sender = {self.sender}, receiver = {self.receiver}, message = {self.message}'


def get_table_count(client: boto3.client) -> Optional[int]:
    """概要
    UserMessageテーブルの行数を返す。テーブルへのアクセスが失敗したらNoneを返す
    Seq の最大値でないのは、scanのシンタックスを失念した＆実装に時間をかけたくないから
    """
    try:
        response = client.scan(
            TableName=TABLE_NAME,
            Select='COUNT'
        )

        print(f'get_record_count: scan response = {response}')

        return int(response['Count'])
    except KeyError:
        return None


def put_message(client: boto3.client, seq: int, user_message: UserMessage) -> bool:
    """概要
    UserMessageテーブルに1行レコードを追加する。処理の成否は真偽値で返す
    """
    try:
        client.put_item(
            TableName='UserMessage',
            Item={
                'seq': {
                    'N': str(seq)
                },
                'sender': {
                    'S': user_message.sender
                },
                'receiver': {
                    'S': user_message.receiver
                },
                'message': {
                    'S': user_message.message
                },
            }
        )

        return True
    except Exception as e:
        print(f'put_message: Error = {e}')

        return False


def lambda_handler(event, context):
    try:
        user_message = UserMessage(event)
        print(user_message)
    except KeyError as ke:
        # 本来はロガーなどを経由して CloudWatch とかで検知できるようにすべき
        print(ke)
        return json.dumps({
            "statusCode": 400,
            "body": json.dumps({
                "message": "Some required parameters are not included",
            }),
        })

    client = boto3.client('dynamodb')

    count = get_table_count(client)

    if count is None:
        seq = 1
    else:
        seq = count + 1

    is_success = put_message(client, seq, user_message)
    if is_success:
        status_code = 200
        message = 'User message is recorded successfully.'
    else:
        status_code = 400
        message = 'Cannot access to DynamoDB table (put_item)'

    return json.dumps({
        "statusCode": status_code,
        "message": message,
    })
