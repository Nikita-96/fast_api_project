# import json
from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep

# from src.init import redis_manager
from src.schema.facilities import FacilitiesAdd
from src.service.facilities import FacilityService

router = APIRouter(prefix="/facilities", tags=["Удобства номера"])


@router.get("", description="Получение всех удобств")
@cache(expire=30)
async def get_facilities(db: DBDep):
    return await FacilityService(db).get_facilities()

    # facilities_from_cache = await redis_manager.get("facilities")
    #
    # if not facilities_from_cache:
    #     facilities = await db.facilities.get_all()
    #     facilities_schemas: list[dict] = [model.model_dump() for model in facilities]
    #     facilities_json = json.dumps(facilities_schemas)
    #     await redis_manager.set("facilities", facilities_json)
    #     return facilities
    # else:
    #     facilities_dicts = json.loads(facilities_from_cache)
    #
    # return facilities_dicts


@router.post("", description="Добавление удобств")
async def add_facilities(db: DBDep, data: FacilitiesAdd):
    facility = await FacilityService(db).add_facilities(data=data)
    return {"status": "OK", "data": facility}
