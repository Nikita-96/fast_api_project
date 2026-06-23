from typing import TypeVar
from pydantic import BaseModel

from src.database import Base


DBModelType = TypeVar("DBModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper:
    db_model: type[DBModelType] = None
    schema: type[SchemaType] = None

    # возвращается модель pydantic
    @classmethod
    def map_to_domain_entity(cls, db_model):
        return cls.schema.model_validate(db_model, from_attributes=True)

    # возвращается модель sqlalchemy
    @classmethod
    def map_to_persistance_entity(cls, data):
        return cls.db_model(**data.model_dump())
