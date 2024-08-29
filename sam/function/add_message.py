import json
import boto3
from data.message import Message, get_count, put_message


def lambda_handler(event, context):
    try:
        msg = Message(event)
        print(msg)
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

    count = get_count(client)

    if count is None:
        seq = 1
    else:
        seq = count + 1

    is_success = put_message(client, seq, msg)
    if is_success:
        status_code = 200
        response_message = 'User message is recorded successfully.'
    else:
        status_code = 400
        response_message = 'Cannot access to DynamoDB table (put_item)'

    return json.dumps({
        "statusCode": status_code,
        "message": response_message,
    })
