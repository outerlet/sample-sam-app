import json
from data.book import Book


def lambda_handler(event, context):
    records = event['Records']
    books = [Book(record['dynamodb']['NewImage']) for record in records]

    for book in books:
        print(f'book = {book}')

    return json.dumps({
        'status_code': 200,
    })
