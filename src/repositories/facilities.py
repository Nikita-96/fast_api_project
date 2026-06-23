from sqlalchemy import select, delete, insert

from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import FacilityDataMapper
from src.schema.facilities import RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    mapper = FacilityDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacility

    async def set_all_facilities(self, room_id: int, facilities_ids: list[int]):
        query = select(self.model.facility_id).filter_by(room_id=room_id)
        result = await self.session.execute(query)
        current_facilities_ids = result.scalars().all()
        facilities_for_delete = list(set(current_facilities_ids) - set(facilities_ids))
        facilities_for_add = list(set(facilities_ids) - set(current_facilities_ids))

        if facilities_for_delete:
            stmt_delete = delete(self.model).filter(
                self.model.room_id == room_id,
                self.model.facility_id.in_(facilities_for_delete),
            )
            await self.session.execute(stmt_delete)

        if facilities_for_add:
            stmt_insert = insert(self.model).values(
                [
                    {"room_id": room_id, "facility_id": facility}
                    for facility in facilities_for_add
                ]
            )

            await self.session.execute(stmt_insert)
