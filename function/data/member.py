from dataclasses import dataclass
from enum import Enum


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
