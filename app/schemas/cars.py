from pydantic import BaseModel, Field
from typing import Optional

class Car(BaseModel):
    id: str = Field(min_length=3, max_length=50)
    model: str = Field(min_length=3, max_length=50)
    brand: str = Field(min_length=3, max_length=50)
    color: str = Field(min_length=3, max_length=50)
    max_speed: int
    mileage: int
    average_consumption: float
    price_sell: float
    price_rent: float
    rent: bool
    sell:bool
    owner_email: Optional[str] = Field(min_length=3, max_length=50)

class VehicleCreate(Car):
    pass

class Vehicle(Car):
    id: int

    class Config:
        orm_mode = True


class Rental(BaseModel):
    user_email: str
    car_id: str
