from pydantic import BaseModel


class Airport(BaseModel):
    city: str
    country: str


class WeekendFlight(BaseModel):
    from_airport: Airport
    destination_airport: Airport
    departure_date: str
    comeback_date: str
    price: float
