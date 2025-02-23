import random

import faker
from src.models import Client

faker = faker.Faker("en_US")


def get_num(lenght):
    return "".join(chr(random.randint(49, 57)) for _ in range(lenght))


def get_str(lenght):
    return "".join(chr(random.randint(97, 122)) for _ in range(lenght))


def create_db_client(num):
    client_list = []
    for _ in range(num):
        name = faker.first_name()
        surname = faker.last_name()
        credit_card = f'{"-".join(get_num(4) for _ in range(4))}'
        car_number = f"{get_str(1)}{get_num(3)}{get_str(2)}163"
        client = Client(
            name=name, surname=surname, credit_card=credit_card, car_number=car_number
        )
        client_list.append(client)
    return client_list
