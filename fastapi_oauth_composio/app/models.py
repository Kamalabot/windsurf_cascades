from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Integer, default=1)
    api_key = Column(String, unique=True, nullable=True)
    api_key_created_at = Column(DateTime, nullable=True)

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    product_name = Column(String, index=True)
    quantity = Column(Integer)
    unit_price = Column(Float)
    total_amount = Column(Float)
    customer_name = Column(String)
