from datetime import date

from fastapi import Body, APIRouter

from src.api.dependencies import DBDep
from src.exceptions import  RoomNotFoundHTTPException, \
    RoomNotFoundException, HotelNotFoundException, HotelNotFoundHTTPException
from src.schema.rooms import RoomEdit, RoomPatchEdit
from src.service.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Комнаты отелей"])


@router.get("/{hotel_id}/rooms", description="Получение всех комнат отеля")
async def get_rooms(hotel_id: int, db: DBDep, date_from: date, date_to: date):
    return await RoomService(db).get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)





@router.get("/{hotel_id}/rooms/{room_id}", description="Получение всех комнат отеля")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        return await RoomService(db).get_room(hotel_id=hotel_id, room_id=room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post("/{hotel_id}/room", description="Добавление комнаты")
async def create_room(hotel_id: int, db: DBDep, room: RoomEdit = Body()):
    try:
        room_data = await RoomService(db).create_room(hotel_id=hotel_id, room=room)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK", "room": room_data}


@router.put("/{hotel_id}/room/{room_id}", description="Изменение данных номера")
async def update_room(hotel_id: int, room_id: int, room_model: RoomEdit, db: DBDep):
    await RoomService(db).update_room(hotel_id=hotel_id, room_id=room_id, room_model=room_model)

    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/room/{room_id}", description="Частичное изменение данных номера"
)
async def patch_room(hotel_id: int, room_id: int, room_model: RoomPatchEdit, db: DBDep):
    await RoomService(db).patch_room(hotel_id=hotel_id, room_id=room_id, room_model=room_model)
    return {"status": "OK"}


@router.delete("/{hotel_id}/room/{room_id}", description="Удаление номера")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await RoomService.delete_room(hotel_id=hotel_id, room_id=room_id)
    return {"status": "OK"}
