import pytest
from src.app import create_app
from src.models import (
    Client,
    ClientParking,
    Parking,
)
from module_30_ci_linters.homework.hw1.src.models import db as _db

url_test = "sqlite://"


@pytest.fixture
def app():
    _app = create_app(url=url_test)

    with _app.app_context():
        _db.create_all()
        client = Client(
            name="name",
            surname="surname",
            credit_card="1111-2222-3333-4444",
            car_number="h336xt163",
        )
        parking = Parking(
            address="address", opened=1, count_places=5, count_available_places=2
        )
        _db.session.add(client)
        _db.session.add(parking)
        _db.session.flush()
        client_parking = ClientParking(
            client_id=client.id,
            parking_id=parking.id,
        )
        _db.session.add(client_parking)
        _db.session.commit()

        yield _app
        _db.session.close()
        _db.drop_all()


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db
        
