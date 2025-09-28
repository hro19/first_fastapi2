from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ProductResultResponse(BaseModel):
    id: str
    generated_at: datetime
    total_price: float
    total_record: int
    average_price: float

    class Config:
        from_attributes = True


__all__ = ["ProductResultResponse"]
