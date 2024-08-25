from typing import Optional
from dataclasses import dataclass
import boto3

TABLE_NAME = 'Message'


@dataclass
class Message:
    sender: str
    receiver: str
    message: str

    def __init__(self, event: dict):
        self.sender = event['sender']
        self.receiver = event['receiver']
        self.message = event['message']

    def __str__(self):
        return f'sender = {self.sender}, receiver = {self.receiver}, message = {self.message}'


def get_count(client: boto3.client) -> Optional[int]:
    """概要
    Messageテーブルの行数を返す。テーブルへのアクセスが失敗したらNoneを返す
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


def put_message(client: boto3.client, seq: int, message: Message) -> bool:
    """概要
    Messageテーブルに1行レコードを追加する。処理の成否は真偽値で返す
    """
    try:
        client.put_item(
            TableName=TABLE_NAME,
            Item={
                'seq': {
                    'N': str(seq)
                },
                'sender': {
                    'S': message.sender
                },
                'receiver': {
                    'S': message.receiver
                },
                'message': {
                    'S': message.message
                },
            }
        )

        return True
    except Exception as e:
        print(f'put_message: Error = {e}')

        return False
