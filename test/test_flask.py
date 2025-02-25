import datetime
import json

import pytest # type: ignore


@pytest.mark.parametrize("route", ["/clients", "/clients/1"])
def test_route_status(client, route):
    rv = client.get(route)
    assert rv.status_code == 200


def test_create_client(client) -> None:
    client_ = json.dumps(
        {
            "name": "Сергей",
            "surname": "Петров",
            "credit_card": "1447-2815-3738-9628",
            "car_number": "s671fo163",
        }
    )
    resp = client.post("/clients", data=client_, content_type="application/json")
    assert resp.status_code == 201


def test_create_parking(client) -> None:
    parking = json.dumps(
        {
            "address": "ТЦ 'Парк-Хаус'",
            "opened": 1,
            "count_places": 5,
            "count_available_places": 5,
        }
    )
    resp = client.post("/parkings", data=parking, content_type="application/json")
    assert resp.status_code == 201


def test_create_client_parking(client) -> None:
    client_parking = json.dumps({"client_id": 1, "parking_id": 1})
    resp = client.post(
        "/client-parkings", data=client_parking, content_type="application/json"
    )
    assert resp.status_code == 201


def test_del_client_parking(client) -> None:
    client_parking = json.dumps(
        {"client_id": 1, "parking_id": 1, "time_out": str(datetime.datetime.utcnow())}
    )
    resp = client.post(
        "/client-parkings", data=client_parking, content_type="application/json"
    )
    assert resp.status_code == 201
