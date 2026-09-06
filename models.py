from database import Base
from sqlalchemy import Column, Integer, String, Float

class EstimateItem(Base):
    __tablename__ = "estimate_items"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)