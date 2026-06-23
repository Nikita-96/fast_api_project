from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep
from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException
from src.schema.bookings import BookingsAdd, BookingsEdit
from src.api.dependencies import UserIdDep
from src.service.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирование номеров"])


@router.get("", description="Получение всех бронирований")
async def get_all_bookings(
    db: DBDep,
    user_id: UserIdDep,
):
    if not user_id:
        raise HTTPException(status_code=403, detail="Пользователь не авторизован")
    return await BookingService(db).get_all_bookings()


@router.get("/me", description="Получение бронирований пользователя")
async def get_me_bookings(db: DBDep, user_id: UserIdDep):
    if not user_id:
        raise HTTPException(status_code=403, detail="Пользователь не авторизован")
    return await BookingService(db).get_me_bookings(user_id=user_id)


@router.post("", description="Бронирование комнаты")
async def add_booking(db: DBDep, data: BookingsEdit, user_id: UserIdDep):
    if not user_id:
        raise HTTPException(status_code=403, detail="Пользователь не авторизован")
    try:
        booking_data = await BookingService(db).add_booking(data=data, user_id=user_id)
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException

    return {"status": "OK", "data": booking_data}
