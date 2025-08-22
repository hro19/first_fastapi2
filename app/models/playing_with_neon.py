from sqlalchemy import Column, Integer, Text, Float
from app.core.database import Base


class PlayingWithNeon(Base):
    __tablename__ = "playing_with_neon"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    value = Column(Float, nullable=True)