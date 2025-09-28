from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, Text

from app.core.database import Base


def _generate_id() -> str:
    return uuid.uuid4().hex


class ProductResult(Base):
    __tablename__ = "product_result"

    id = Column(Text, primary_key=True, default=_generate_id)
    generated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    total_price = Column(Float, nullable=False)
    total_record = Column(Integer, nullable=False)
    average_price = Column(Float, nullable=False)


__all__ = ["ProductResult"]
