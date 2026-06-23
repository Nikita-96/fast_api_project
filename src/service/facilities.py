from src.schema.facilities import FacilitiesAdd
from src.service.base import BaseService


class FacilityService(BaseService):
    async def get_facilities(self):
        return await self.db.facilities.get_all()

    async def add_facilities(self,data: FacilitiesAdd):
        facility = await self.db.facilities.add(data)
        await self.db.commit()
        return facility
