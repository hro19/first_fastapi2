from pydantic import BaseModel
from typing import Optional


class PlayingWithNeonBase(BaseModel):
    name: str
    value: Optional[float] = None


class PlayingWithNeonCreate(PlayingWithNeonBase):
    pass


class PlayingWithNeonResponse(PlayingWithNeonBase):
    id: int

    class Config:
        from_attributes = True