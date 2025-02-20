import datetime

from flask import Flask, jsonify, request

from create_data import create_db_client
from models import Client, ClientParking, Parking, db

URL_MAIN = "postgresql+psycopg2://admin:admin@localhost/skillbox_mod_30"


def create_app(url=URL_MAIN):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    @app.before_request
    def before_request_func():
        db.drop_all()
        db.create_all()

        db.session.bulk_save_objects(create_db_client(10))
        db.session.commit()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.route("/clients", methods=["GET"])
    def get_clients():
        client_parking_list = []
        clients = db.session.query(Client).all()
        for client in clients:
            obj = client.to_json()
            obj["parking"] = [
                client_parking.parking.to_json() for client_parking in client.parking
            ]
            client_parking_list.append(obj)
        return jsonify(client_parking_list), 200

    @app.route("/clients/<int:client_id>", methods=["GET"])
    def get_client_id(client_id):
        client = db.session.query(Client).get(client_id)
        obj = client.to_json()
        obj["parking"] = [
            client_parking.parking.to_json() for client_parking in client.parking
        ]
        return jsonify(obj), 200

    @app.route("/clients", methods=["POST"])
    def create_clients():
        name = request.json["name"]
        surname = request.json["surname"]
        credit_card = request.json["credit_card"]
        car_number = request.json["car_number"]
        client = Client(
            name=name, surname=surname, credit_card=credit_card, car_number=car_number
        )

        db.session.add(client)
        db.session.commit()

        return "OK", 201

    @app.route("/parkings", methods=["POST"])
    def create_parkings():
        address = request.json["address"]
        opened = request.json["opened"]
        count_places = request.json["count_places"]
        count_available_places = request.json["count_available_places"]

        parking = Parking(
            address=address,
            opened=opened,
            count_places=count_places,
            count_available_places=count_available_places,
        )

        db.session.add(parking)
        db.session.commit()

        return "OK", 201

    @app.route("/client-parkings", methods=["POST"])
    def create_client_parkings():
        client_id = request.json["client_id"]
        parking_id = request.json["parking_id"]

        client = db.session.query(Client).get(client_id)
        parking = db.session.query(Parking).get(parking_id)
        client_parking = ClientParking.search_client_parking(
            client_id=client.id, parking_id=parking.id
        )

        if client is None:
            return f"Клиент с id {client_id}, не зарегистрирован"
        elif parking is None:
            return f"Парковка с id {parking_id}, не зарегистрирован"
        elif parking.opened is False:
            return f"Парковка с id {parking_id}, не работает"
        elif parking.count_available_places <= 0:
            return "Извините, свободных мест нет"
        elif client_parking:
            return "Вашу машину уже припарковали"
        else:
            client_parkings = ClientParking(client_id=client_id, parking_id=parking_id)
            parking.count_available_places = parking.count_available_places - 1
            db.session.add(client_parkings)
            db.session.commit()

        return "OK", 201

    @app.route("/client-parkings", methods=["DELETE"])
    def del_client_parkings():
        client_id = request.json["client_id"]
        parking_id = request.json["parking_id"]

        client = db.session.query(Client).get(client_id)
        parking = db.session.query(Parking).get(parking_id)
        client_parking = ClientParking.search_client_parking(
            client_id=client.id, parking_id=parking.id
        )
        if client is None:
            return f"Клиент с id {client_id}, не зарегистрирован"
        elif client.car_number is None:
            return "БЕЗ КАРТЫ НЕ УЙДЕШЬ"
        elif parking is None:
            return f"Парковка с id {parking_id}, не зарегистрирован"
        elif client_parking is None:
            return "Ваша машина давно уехала"
        else:
            client_parking.time_out = datetime.datetime.utcnow()
            parking.count_available_places = parking.count_available_places + 1
            db.session.commit()

        return "OK", 201

    return app
