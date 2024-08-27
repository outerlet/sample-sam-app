from dataclasses import dataclass


@dataclass
class Book:
    seq: int
    title: str
    publisher: str
    price: int

    def __init__(self, record: dict):
        self.seq = int(record['seq']['N'])
        self.title = record['title']['S']
        self.publisher = record['publisher']['S']
        self.price = int(record['price']['N'])

    def __str__(self):
        return f'{self.seq},{self.title},{self.publisher},{self.price}'
