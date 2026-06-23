from datetime import date
from fastapi import HTTPException

from fastapi import Body, APIRouter, Query
from fastapi_cache.decorator import cache

from src.exceptions import ObjectNotFoundException
from src.schema.hotels import HotelAdd, HotelPatch
from src.api.dependencies import pagDep, DBDep
from src.service.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/", description="Получение всех отелей")
@cache(expire=10)
async def get_hotels(
    page_data: pagDep,
    db: DBDep,
    date_from: date,
    date_to: date,
    title: str | None = Query(None, description="Наименование отеля"),
    location: str | None = Query(None, description="Расположение отеля"),
):
    return await HotelService(db).get_filtered_by_time(
        page_data=page_data,
        date_from=date_from,
        date_to=date_to,
        title=title,
        location=location
    )
    # return await db.hotels.get_all(
    #     location=location,
    #     title=title,
    #     limit=per_page,
    #     offset=per_page * (page_data.page - 1)
    # )


@router.get("/{hotel_id}", description="Получение 1 отеля")
async def get_one_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Отель не найден")


@router.post("/")
async def create_hotel(
    db: DBDep,
    hotel: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Нью-Йорк",
                "value": {"title": "New York", "location": "york"},
            },
            "2": {
                "summary": "Астрахань",
                "value": {"title": "Астрахань лучший город", "location": "Astra"},
            },
        }
    ),
):
    hotel_data = await HotelService(db).add_hotel(hotel)
    return {"status": "OK", "hotel": hotel_data}


@router.put("/{hotel_id}")
async def update_hotel(hotel_id: int, hotel_model: HotelAdd, db: DBDep):
    await HotelService(db).update_hotel(hotel_id=hotel_id, hotel_model=hotel_model)
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotels(hotel_id: int, db: DBDep):
    await HotelService(db).delete_hotel(hotel_id)
    return {"status": "OK"}


@router.patch("/{hotel_id}")
async def patch_hotel(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    await HotelService(db).partially_update_hotel(hotel_id=hotel_id,hotel_data=hotel_data)
    return {"status": "OK"}
