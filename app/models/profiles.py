from sqlalchemy import Column, Text, Integer
from sqlalchemy.orm import relationship
from app.core.database import Base


class Profile(Base):
    __tablename__ = "profiles"
    
    id = Column(Text, primary_key=True)
    image = Column(Text, nullable=True)
    name = Column(Text, nullable=True)
    gender = Column(Text, nullable=True)
    age = Column(Integer, nullable=True)
    role = Column(Text, nullable=False, default='user')
    password = Column(Text, nullable=False)
    
    # Relationship to products
    products = relationship("Product", back_populates="profile")