from pydantic import BaseModel
from datetime import date
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class UserApiKey(BaseModel):
    api_key: str

class SaleBase(BaseModel):
    date: date
    product_name: str
    quantity: int
    unit_price: float
    total_amount: float
    customer_name: str

class SaleCreate(SaleBase):
    pass

class Sale(SaleBase):
    id: int

    class Config:
        from_attributes = True
