from pydantic import BaseModel
from fastapi import Depends, Query
from typing import Annotated

class Pages(BaseModel):
    page: Annotated[int, Query(1, ge=1)]
    per_page: Annotated[int, Query(10, ge=1, le=30)]

pagDep = Annotated[Pages, Depends()]