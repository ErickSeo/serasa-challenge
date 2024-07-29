from datetime import datetime
from pydantic import BaseModel


class TripModel(BaseModel):
    key: str
    pickup_datetime: datetime
    pickup_longitude: float
    pickup_latitude: float
    dropoff_longitude: float
    dropoff_latitude: float
    passenger_count: int
    fare_amount: float
