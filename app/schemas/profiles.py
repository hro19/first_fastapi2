from pydantic import BaseModel
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .products import ProductResponse


class ProfileBase(BaseModel):
    image: Optional[str] = None
    name: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    role: str = "user"


class ProfileCreate(ProfileBase):
    pass


class ProfileResponse(ProfileBase):
    id: str
    products: List["ProductResponse"] = []

    class Config:
        from_attributes = True