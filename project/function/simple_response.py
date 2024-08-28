import json

NUMBER_PAIR = {
    1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five',
    6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten'
}


def lambda_handler(event, context):
    status_code: int = 200
    message: str = ''

    try:
        key = int(event['queryStringParameters']['number'])

        number_text = NUMBER_PAIR.get(key)

        if number_text is not None:
            message = number_text
        else:
            message = 'A numeric value, but not a value between 1 and 10'

        status_code = 200
    except KeyError as ke:
        print(f'KeyError: {ke}')
        status_code = 400
        message = 'Key "number" is not found'
    except ValueError as ve:
        print(f'ValueError: {ve}')
        status_code = 400
        message = 'Value of "number" is not number'
    finally:
        return {
            'statusCode': status_code,
            'body': json.dumps({
                'message': message
            })
        }
