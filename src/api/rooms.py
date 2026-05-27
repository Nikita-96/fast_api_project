from datetime import date

from fastapi import Body, APIRouter

from src.api.dependencies import DBDep
from src.schema.facilities import RoomFacilityAdd
from src.schema.rooms import RoomAdd, RoomEdit, RoomPatch, RoomPatchEdit

router = APIRouter(prefix="/hotels", tags=["Комнаты отелей"])

@router.get("/{hotel_id}/rooms", description="Получение всех комнат отеля")
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date,
        date_to: date
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id,date_to=date_to,date_from=date_from)


@router.get("/{hotel_id}/rooms/{room_id}", description="Получение всех комнат отеля")
async def get_room(
        hotel_id: int,
        room_id: int,
        db: DBDep
):
    return await db.rooms.get_one_or_none(hotel_id=hotel_id,id=room_id)


@router.post("/{hotel_id}/room",description="Добавление комнаты")
async def create_room(
        hotel_id: int,
        db: DBDep,
        room: RoomEdit = Body()
):
    _room = RoomAdd(hotel_id=hotel_id, **room.model_dump())
    # async with async_session_maker() as session:
    room_data = await db.rooms.add(_room)
    rooms_facilities_data = [RoomFacilityAdd(room_id=room_data.id, facility_id=f_id) for f_id in room.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"status": "OK", "room": room_data}

@router.put("/{hotel_id}/room/{room_id}", description="Изменение данных номера")
async def update_room(
        hotel_id: int,
        room_id: int,
        room_model: RoomEdit,
        db: DBDep
):
    _room_model = RoomAdd(hotel_id=hotel_id, **room_model.model_dump())
    # async with async_session_maker() as session:
    await db.rooms.edit(data=_room_model,id=room_id)
    await db.rooms_facilities.set_all_facilities(room_id=room_id, facilities_ids=room_model.facilities_ids)
    await db.commit()

    return {"status": "OK"}

@router.patch("/{hotel_id}/room/{room_id}", description="Частичное изменение данных номера")
async def patch_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchEdit,
        db: DBDep
):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)

    # async with async_session_maker() as session:
    await db.rooms.edit(data=_room_data, exclude_unset=True,id=room_id, hotel_id=hotel_id)
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_all_facilities(room_id=room_id,facilities_ids=room_data.facilities_ids)
    await db.commit()
    return {"status": "OK"}

@router.delete("/{hotel_id}/room/{room_id}", description="Удаление номера")
async def delete_room(
        hotel_id: int, room_id: int, db: DBDep
):
    # async with async_session_maker() as session:
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}
