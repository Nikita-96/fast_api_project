from pydantic import BaseModel, ConfigDict
from datetime import date


class BookingsEdit(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingsAdd(BookingsEdit):
    user_id: int
    price: int


class Bookings(BookingsAdd):
    id: int
    total_cost: int

    model_config = ConfigDict(from_attributes=True)
