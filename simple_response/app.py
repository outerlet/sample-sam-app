import json


def lambda_handler(event, context):
    status_code: int = 200
    message: str = ""

    try:
        number = int(event["number"])

        if number == 1:
            message = "One"
        elif number == 2:
            message = "Two"
        elif number == 3:
            message = "Three"
        elif number == 4:
            message = "Four"
        elif number == 5:
            message = "Five"
        else:
            message = "A numeric value, but not a value between 1 and 5"

        status_code = 200
    except KeyError as ke:
        status_code = 400
        message = "Key 'number' is not found"
    except ValueError as ve:
        status_code = 400
        message = "Value of 'number' is not number"
    finally:
        return {
            "statusCode": status_code,
            "body": json.dumps({
                "message": message
            })
        }
