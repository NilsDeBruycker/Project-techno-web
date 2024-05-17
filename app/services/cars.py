from uuid import uuid4
from sqlalchemy import select, ForeignKey
from sqlalchemy.orm import relationship

from app.schemas import cars
from app.database import Session
from app.models.car import Car
from app.models import Rental
from app.schemas.cars import Car as CarSchema
from app.schemas import Rental as RentalSchema


def save_rental(new_rental: RentalSchema):
    with Session() as session:
        rental_entity = Rental(
            user_email=new_rental.user_email,
            car_id=new_rental.car_id
        )
        session.add(rental_entity)
        session.commit()
def save_car(new_car: CarSchema):
    with Session() as session:
        new_car_entity = Car(
            id=uuid4().hex,
            brand=new_car.brand,
            model=new_car.model,
            price=new_car.price,
            owner=new_car.owner,
            status=new_car.status,
            year=new_car.year,
            color=new_car.color,
        )
        session.add(new_car_entity)
        session.commit()

def get_public_cars():
    with Session() as session:
        statement = select(Car).filter(Car.status == "available")
        cars_data = session.scalars(statement).unique().all()
    return [
        Car(
            id=car.id,
            brand=car.brand,
            model=car.model,
            price=car.price,
            owner=car.owner,
            status=car.status,
            year=car.year,
            color=car.color,
        )
        for car in cars_data
    ]

def get_own_cars(user):
    with Session() as session:
        statement = select(Car).filter(Car.owner == user.email)
        cars_data = session.scalars(statement).unique().all()
    return [
        Car(
            id=car.id,
            brand=car.brand,
            model=car.model,
            price=car.price,
            owner=car.owner,
            status=car.status,
            year=car.year,
            color=car.color,
        )
        for car in cars_data
    ]

def get_all_cars() -> list[Car]:
    with Session() as session:
        statement = select(Car)
        cars_data = session.scalars(statement).unique().all()
    return [
        Car(
            id=car.id,
            brand=car.brand,
            model=car.model,
            price=car.price,
            owner=car.owner,
            status=car.status,
            year=car.year,
            color=car.color,
        )
        for car in cars_data
    ]

def delete_car_by_id(car_id:str):
    with Session() as session:
        statement=select(Car).filter(Car.id == car_id)
        car=session.scalars(statement).one()
        session.delete(car)
        session.commit()

def is_car_exist(car_id:str):
    with Session() as session:
        statement=select(Car).filter(Car.id == car_id)
        car=session.scalar(statement)
        return car is not None

def get_car_by_id(car_id):
    with Session() as session:
        statement=select(Car).filter(Car.id == car_id)
        car=session.scalars(statement).one_or_none()
        if car:
            return Car(
                id=car.id,
                brand=car.brand,
                model=car.model,
                price=car.price,
                owner=car.owner,
                status=car.status,
                year=car.year,
                color=car.color,
            )
        return None

def modify_car_by_id(car_id: str, modified_car) -> Car | None:
    with Session() as session:
        statement=select(Car).filter(Car.id == car_id)
        car=session.scalars(statement).one_or_none()
        if car:
            car.owner = modified_car.get("owner", car.owner)
            car.brand = modified_car.get("brand", car.brand)
            car.model = modified_car.get("model", car.model)
            car.status = modified_car.get("status", car.status)
            car.price = modified_car.get("price", car.price)
            car.year = modified_car.get("year", car.year)
            car.color = modified_car.get("color", car.color)
            session.commit()
            return car
        return None



def rent_car(user_email: str, car_id: str):
    with Session() as session:
        car = session.query(Car).filter(Car.id == car_id, Car.status == "available").one_or_none()
        if car:
            rental = Rental(user_email=user_email, car_id=car_id)
            session.add(rental)
            car.status = "rented"
            session.commit()
            return True
        return False

def return_car(user_email: str, car_id: str):
    with Session() as session:
        rental = session.query(Rental).filter(Rental.user_email == user_email, Rental.car_id == car_id).one_or_none()
        if rental:
            car = session.query(Car).filter(Car.id == car_id).one()
            car.status = "available"
            session.delete(rental)
            session.commit()
            return True
        return False

def get_rented_cars(user_email: str):
    with Session() as session:
        statement = select(Car).join(Rental).filter(Rental.user_email == user_email)
        cars_data = session.scalars(statement).unique().all()
    return [
        Car(
            id=car.id,
            brand=car.brand,
            model=car.model,
            price=car.price,
            owner=car.owner,
            status=car.status,
            year=car.year,
            color=car.color,
        )
        for car in cars_data
    ]
