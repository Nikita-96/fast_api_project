from src.models.bookings import BookingsOrm
from src.models.facilities import FacilitiesOrm
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm
from src.repositories.mappers.base import DataMapper
from src.schema.bookings import Bookings
from src.schema.facilities import Facilities
from src.schema.hotels import Hotel
from src.schema.rooms import Room, RoomWithRels
from src.schema.users import User, UserWithHashedPassword


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel

class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Room

class RoomDataWithRelsMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomWithRels

class BookingDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = Bookings

class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User

class UserWithHashDataMapper(DataMapper):
    db_model = UsersOrm
    schema = UserWithHashedPassword

class FacilityDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = Facilities

