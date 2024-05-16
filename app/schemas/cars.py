from pydantic import BaseModel

class VehicleBase(BaseModel):
    model: str
    brand: str
    color: str
    max_speed: int
    mileage: int
    average_consumption: float

class VehicleCreate(VehicleBase):
    pass

class Vehicle(VehicleBase):
    id: int

    class Config:
        orm_mode = True
