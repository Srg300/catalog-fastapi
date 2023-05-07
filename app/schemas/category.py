from typing import Optional, List

from pydantic import BaseModel


class CatalogBase(BaseModel):
    id: int


class CatalogOut(CatalogBase):
    avatars: List[str]
    expert_count: Optional[int]
    title: str
    slug: str
    description: str
    order: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ShortCategory(CatalogBase):
    title: str
