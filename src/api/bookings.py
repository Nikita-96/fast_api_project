from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep
from src.schema.bookings import BookingsAdd, BookingsEdit
from src.api.dependencies import UserIdDep

router = APIRouter(prefix="/bookings", tags=['Бронирование номеров'])

@router.get("",description="Получение всех бронирований")
async def get_all_bookings(
        db: DBDep,
        user_id: UserIdDep,
):
    if not user_id:
        raise HTTPException(status_code=403, detail="Пользователь не авторизован")
    return await db.bookings.get_all()

@router.get("/me",description="Получение бронирований пользователя")
async def get_me_bookings(db: DBDep, user_id: UserIdDep):
    if not user_id:
        raise HTTPException(status_code=403, detail="Пользователь не авторизован")
    return await db.bookings.get_filtered(user_id=user_id)

@router.post("", description="Бронирование комнаты")
async def add_booking(db: DBDep, data: BookingsEdit, user_id: UserIdDep):
    if not user_id:
        raise HTTPException(status_code=403, detail="Пользователь не авторизован")
    room = await db.rooms.get_one_or_none(id=data.room_id)
    hotel_id = room.hotel_id
    _data = BookingsAdd(user_id=user_id, price=room.price, **data.model_dump())
    booking_data = await db.bookings.add_booking(_data, hotel_id=hotel_id)
    await db.commit()

    return {"status": "OK","data": booking_data}