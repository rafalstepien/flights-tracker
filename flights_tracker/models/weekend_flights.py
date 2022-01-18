from enum import Enum

from pydantic import BaseModel


class Airport(BaseModel):
    city: str
    country: str
    code: str


class WhichWay(Enum):
    THERE = "There"
    BACK = "Back"


class OneWayFlight(BaseModel):
    which_way: WhichWay
    flight_length: str
    price_euro: str
    number_of_changes: int

    departure_date: str
    departure_time: str
    departure_airport: Airport

    arrival_time: str
    arrival_airport: Airport

    class Config:
        use_enum_values = True


class Flight(BaseModel):
    flight_there: OneWayFlight
    flight_back: OneWayFlight
    airline: str


# TODO: Handle overnight fligts
