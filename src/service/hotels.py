from datetime import date

from src.api.dependencies import pagDep
from src.exceptions import check_date_to_after_date_from, HotelNotFoundException, ObjectNotFoundException
from src.schema.hotels import HotelAdd, HotelPatch, Hotel
from src.service.base import BaseService


class HotelService(BaseService):
    async def get_filtered_by_time(
        self,
        page_data: pagDep,
        date_from: date,
        date_to: date,
        title: str | None,
        location: str | None,
    ):
        check_date_to_after_date_from(date_to=date_to, date_from=date_from)
        per_page = page_data.per_page or 5
        return await self.db.hotels.get_filtered_by_time(
            date_to=date_to,
            date_from=date_from,
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (page_data.page - 1),
        )

    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def add_hotel(self, hotel: HotelAdd):
        hotel_data = await self.db.hotels.add(hotel)
        # #  формирование запроса SQL со значениями, которые добавляются
        # print(add_hotel_stmt.compile(compile_kwargs={"literal_binds":True}))
        await self.db.commit()
        return hotel_data

    async def update_hotel(self, hotel_id: int, hotel_model: HotelAdd):
        await self.db.hotels.edit(data=hotel_model, id=hotel_id)
        await self.db.commit()

    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.hotels.commit()

    async def partially_update_hotel(self, hotel_id: int, hotel_data: HotelPatch):
        await self.db.hotels.edit(data=hotel_data, exclude_unset=True, id=hotel_id)
        await self.db.commit()

    async def get_hotel_with_check(self, hotel_id: int) -> Hotel:
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
