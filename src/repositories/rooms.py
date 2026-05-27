from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomDataWithRelsMapper, RoomDataMapper
from src.repositories.utils import rooms_ids_free
from src.models.rooms import RoomsOrm



class RoomRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

    async def get_filtered_by_time(
            self,
           hotel_id: int,
           date_from: date,
           date_to: date
    ):
        rooms_ids = rooms_ids_free(hotel_id=hotel_id,date_from=date_from, date_to=date_to)
        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids))
        )
        result = await self.session.execute(query)

        return [RoomDataWithRelsMapper.map_to_domain_entity(model) for model in result.unique().scalars().all()]


    async def get_one_or_none(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        res = result.scalars().one_or_none()
        if not res:
            return None
        return RoomDataWithRelsMapper.map_to_domain_entity(res)



    # async def get_all(self, **filter_by):
    #     query = select(self.model).filter_by(**filter_by)
    #     result = await self.session.execute(query)
    #
    #     return [self.schema.model_validate(row, from_attributes=True) for row in result.scalars().all()]
