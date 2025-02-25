from typing import Any, Dict

from flask_sqlalchemy import SQLAlchemy  # type: ignore

db = SQLAlchemy()


class Client(db.Model):  # type: ignore
    __tablename__ = "client"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    credit_card = db.Column(db.String(20))
    car_number = db.Column(db.String(9))

    parking = db.relationship(
        "ClientParking", back_populates="client", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"Клиент {self.name} {self.surname} "
            f"{self.credit_card} {self.car_number}"
        )

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Parking(db.Model):  # type: ignore
    __tablename__ = "parking"
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    opened = db.Column(db.Boolean)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)

    client = db.relationship(
        "ClientParking", back_populates="parking", cascade="all, delete-orphan"
    )

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return (
            f"Парковка {self.address} {self.opened} "
            f"{self.count_places} {self.count_available_places}"
        )


class ClientParking(db.Model):  # type: ignore
    __tablename__ = "client_parking"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))
    parking_id = db.Column(db.Integer, db.ForeignKey("parking.id"))
    time_in = db.Column(db.DateTime, default=db.func.now())
    time_out = db.Column(db.DateTime)

    client = db.relationship(
        "Client",
        back_populates="parking",
    )
    parking = db.relationship("Parking", back_populates="client")

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def search_client_parking(cls, client_id=client_id, parking_id=parking_id):
        client_parking = db.session.query(cls).where(
            (cls.client_id == client_id) &
            (cls.parking_id == parking_id) &
            (cls.time_out is None)
        )

        return client_parking.one_or_none()
