from pydantic import BaseModel

class Car(BaseModel):
    model: str
    brand: str
    color: str
    max_speed: int
    mileage: int
    average_consumption: float
    price: float

class VehicleCreate(Car):
    pass

class Vehicle(Car):
    id: int

    class Config:
        orm_mode = True


class Rental(BaseModel):
    user_email: str
    car_id: str
