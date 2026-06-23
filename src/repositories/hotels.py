from datetime import date

from sqlalchemy import select, func

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import HotelDataMapper
from src.repositories.utils import rooms_ids_free
from src.models.hotels import HotelsOrm


class HotelRepository(BaseRepository):
    model = HotelsOrm
    # schema = Hotel
    mapper = HotelDataMapper
    # async def get_all(
    #     self,
    #     location,
    #     title,
    #     limit,
    #     offset
    # ):
    #     query = select(HotelsOrm)
    #     if location:
    #         query = query.where(func.lower(HotelsOrm.location).contains(location))
    #     if title:
    #         query = query.where(func.lower(HotelsOrm.title).contains(title))
    #     query = (
    #         query
    #         .limit(limit)
    #         .offset(offset)
    #     )
    #     result = await self.session.execute(query)
    #     # return result.scalars().all()
    #
    #     return [self.schema.model_validate(row, from_attributes=True) for row in result.scalars().all()]

    async def get_filtered_by_time(
        self, date_from: date, date_to: date, location, title, limit, offset
    ):
        rooms_ids_free_hotels = rooms_ids_free(date_from=date_from, date_to=date_to)
        hotels_ids = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_free_hotels))
        )
        hotels = select(HotelsOrm).filter(HotelsOrm.id.in_(hotels_ids))

        if location:
            hotels = hotels.where(func.lower(HotelsOrm.location).contains(location))
        if title:
            hotels = hotels.where(func.lower(HotelsOrm.title).contains(title))
        hotels = hotels.limit(limit).offset(offset)
        result = await self.session.execute(hotels)
        return [self.mapper.map_to_domain_entity(row) for row in result.scalars().all()]
