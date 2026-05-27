from datetime import date

from fastapi import Body, APIRouter, Query
from fastapi_cache.decorator import cache

from src.schema.hotels import HotelAdd, HotelPatch
from src.api.dependencies import pagDep, DBDep



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
    per_page = page_data.per_page or 5
    return await db.hotels.get_filtered_by_time(
        date_to=date_to,
        date_from=date_from,
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (page_data.page - 1)
    )
    # return await db.hotels.get_all(
    #     location=location,
    #     title=title,
    #     limit=per_page,
    #     offset=per_page * (page_data.page - 1)
    # )

@router.get("/{hotel_id}", description="Получение 1 отеля")
async def get_one_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)

@router.post("/")
async def create_hotel(db: DBDep, hotel: HotelAdd = Body(
    openapi_examples={
        "1": {
            "summary": "Нью-Йорк", "value": {
                    "title": "New York", "location": "york"
                }
        },
        "2": {"summary": "Астрахань", "value": {
                    "title": "Астрахань лучший город", "location": "Astra"
                }
        }
    })):
    hotel_data = await db.hotels.add(hotel)
    # #  формирование запроса SQL со значениями, которые добавляются
    # print(add_hotel_stmt.compile(compile_kwargs={"literal_binds":True}))
    await db.commit()
    return {"status": "OK", 'hotel': hotel_data}



@router.put("/{hotel_id}")
async def update_hotel(hotel_id: int, hotel_model: HotelAdd, db: DBDep):
    await db.hotels.edit(data=hotel_model, id=hotel_id)
    await db.commit()

    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotels(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.hotels.commit()

    return {"status": "OK"}

@router.patch("/{hotel_id}")
async def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPatch,
        db: DBDep
):
    await db.hotels.edit(data=hotel_data,exclude_unset=True, id=hotel_id)
    await db.commit()

    return {"status": "OK"}

