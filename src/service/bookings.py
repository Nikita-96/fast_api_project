from src.api.dependencies import UserIdDep
from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException, RoomNotFoundException
from src.schema.bookings import BookingsEdit, BookingsAdd
from src.service.base import BaseService


class BookingService(BaseService):
    async def get_all_bookings(self):
        return await self.db.bookings.get_all()

    async def get_me_bookings(self, user_id: UserIdDep):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def add_booking(self, data: BookingsEdit, user_id: UserIdDep):
        try:
            room = await self.db.rooms.get_one_or_none(id=data.room_id)
        except ObjectNotFoundException as ex:
            raise RoomNotFoundException from ex
        hotel_id = room.hotel_id
        _data = BookingsAdd(user_id=user_id, price=room.price, **data.model_dump())
        booking_data = await self.db.bookings.add_booking(_data, hotel_id=hotel_id)
        await self.db.commit()
        return booking_data
