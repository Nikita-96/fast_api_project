from fastapi import Body, APIRouter
from schema.hotels import Hotel, HotelPatch
from schema.dependencies import pagDep


router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name":"sochi"},
    {"id": 2, "title": "Дубай","name":"dubay"},
    {"id": 3, "title": "Астрахань", "name": "astra"},
    {"id": 4, "title": "Дубайск", "name": "dubaysk"},
    {"id": 5, "title": "Волга", "name": "volg"},
    {"id": 6, "title": "Днепровск", "name": "dne"},
    {"id": 7, "title": "Енота", "name": "s"},
    {"id": 8, "title": "Питер", "name": "d"},
]

# @router.get("/hotels")
# def get_hotels(
#         id: int | None,
#         title: str | None = Query(None,description="Название отеля"),
# ):
#     return [hotel for hotel in hotels if hotel["title"] == title and hotel["id"] == id]

@router.get("/")
def get_hotels(page_data: pagDep):

    return hotels[page_data.per_page * (page_data.page - 1):][:page_data.per_page]


@router.delete("/{hotel_id}")
def delete_hotels(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]

    return {"status": "OK"}


@router.post("/")
def create_hotel(hotel: Hotel = Body(openapi_examples={"1": {"summary": "Нью-Йорк", "value": {
    "title": "New York", "name": "york"}}, "2": {"summary": "Астрахань", "value": {
    "title": "Астрахань лучший город", "name": "Astra"}}})):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel.title,
        "name": hotel.name
    })
    return {"status": "OK"}

@router.put("/{hotel_id}")
def update_hotel(hotel_id: int, hotel_model: Hotel):
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['title'] = hotel_model.title
            hotel['name'] = hotel_model.name

    return {"status": "OK"}

@router.patch("/{hotel_id}")
def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPatch
):
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            if hotel_data.title:
                hotel['title'] = hotel_data.title
            if hotel_data.name:
                hotel['name'] = hotel_data.name

    return {"status": "OK"}