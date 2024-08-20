from typing import Optional
import json
import boto3

TABLE_NAME = 'UserMessage'


def get_record_count(client: boto3.client) -> Optional[int]:
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


def put_message(client: boto3.client, seq: int, sender: str, receiver: str, message: str) -> bool:
    """概要
    UserMessageテーブルに1行レコードを追加する。処理の成否は真偽値で返す
    """
    print(f'put_message: seq = {seq}, sender = {sender}, receiver = {receiver}, message = {message}')

    try:
        client.put_item(
            TableName='UserMessage',
            Item={
                'Seq': {
                    'N': str(seq)
                },
                'Sender': {
                    'S': sender
                },
                'receiver': {
                    'S': receiver
                },
                'message': {
                    'S': message
                },
            }
        )

        return True
    except Exception as e:
        print(f'put_message: Error = {e}')

        return False


def lambda_handler(event, context):
    try:
        sender = event['sender']
        receiver = event['receiver']
        message = event['message']

        print(f'Arguments: sender = {sender}, receiver = {receiver}, message = {message}')
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

    count = get_record_count(client)

    if count is None:
        new_count = 1
    else:
        new_count = count + 1

    is_success = put_message(client, new_count, sender, receiver, message)
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
