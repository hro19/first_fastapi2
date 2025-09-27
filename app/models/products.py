from sqlalchemy import Column, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Text, primary_key=True)
    name = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=True)
    category = Column(Text, nullable=True)
    profile_id = Column(Text, ForeignKey("profiles.id"), nullable=True)
    
    # Relationship to profile
    profile = relationship("Profile", back_populates="products")
