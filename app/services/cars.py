from uuid import uuid4
from sqlalchemy import select, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Session
from app.models.car import Vehicle
from app.models.car import  Rental
from app.schemas.cars import Car as CarSchema
from app.schemas.cars import Rental as RentalSchema

# Function to save a new rental
def save_rental(new_rental: RentalSchema):
    with Session() as session:
        rental_entity = Rental(
            user_email=new_rental.user_email,
            car_id=new_rental.car_id
        )
        session.add(rental_entity)
        session.commit()

# Function to save a new car
def save_car(new_car: CarSchema):
    with Session() as session:
        new_car_entity = Vehicle(
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

# Function to get all public cars
def get_public_cars():
    with Session() as session:
        statement = select(Vehicle).filter(Vehicle.status == "available")
        cars_data = session.scalars(statement).unique().all()
    return [
        Vehicle(
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

# Function to get all cars owned by a user
def get_own_cars(user):
    with Session() as session:
        statement = select(cars).filter(cars.owner == user.email)
        cars_data = session.scalars(statement).unique().all()
    return [
        cars(
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

# Function to get all cars
def get_all_cars() -> list[cars]:
    with Session() as session:
        statement = select(cars)
        cars_data = session.scalars(statement).unique().all()
    return [
        cars(
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

# Function to delete a car by its ID
def delete_car_by_id(car_id: str):
    with Session() as session:
        statement = select(cars).filter(cars.id == car_id)
        car = session.scalars(statement).one()
        session.delete(car)
        session.commit()

# Function to check if a car exists by its ID
def is_car_exist(car_id: str):
    with Session() as session:
        statement = select(cars).filter(cars.id == car_id)
        car = session.scalar(statement)
        return car is not None

# Function to get a car by its ID
def get_car_by_id(car_id):
    with Session() as session:
        statement = select(cars).filter(cars.id == car_id)
        car = session.scalars(statement).one_or_none()
        if car:
            return cars(
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

# Function to modify a car by its ID
def modify_car_by_id(car_id: str, modified_car) -> cars | None:
    with Session() as session:
        statement = select(cars).filter(cars.id == car_id)
        car = session.scalars(statement).one_or_none()
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

# Function to rent a car
def rent_car(user_email: str, car_id: str):
    with Session() as session:
        car = session.query(cars).filter(cars.id == car_id, cars.status == "available").one_or_none()
        if car:
            rental = Rental(user_email=user_email, car_id=car_id)
            session.add(rental)
            car.status = "rented"
            session.commit()
            return True
        return False

# Function to return a rented car
def return_car(user_email: str, car_id: str):
    with Session() as session:
        rental = session.query(Rental).filter(Rental.user_email == user_email, Rental.car_id == car_id).one_or_none()
        if rental:
            car = session.query(cars).filter(cars.id == car_id).one()
            car.status = "available"
            session.delete(rental)
            session.commit()
            return True
        return False

# Function to get all cars rented by a user
def get_rented_cars(user_email: str):
    with Session() as session:
        statement = select(Vehicle).join(Rental).filter(Rental.user_email == user_email)
        cars_data = session.scalars(statement).unique().all()
    return [
        Vehicle(
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
#Function search of 
def search(search_therm: str):
    with Session() as session:
        statement=select(Vehicle)
        cars = session.scalars(statement).all()
        selected_cars=[]
        for car in cars:
            if (search_therm!=''):
                if((car.make==search_therm or
                    search_therm==car.model or
                    search_therm==car.color)
                    and not( car.rentals and car.sales)):

                    
                
                    selected_cars.append(Vehicle(
                        id=car.id,
                        make=car.make,
                        model=car.model,
                        #price=car.price,
                        owner_email=car.owner_email,
                        max_speed=car.max_speed,
                        mileage=car.mileage,
                        average_consumption=car.average_consumption,
                        color=car.color,
                        sales=False,
                        rentals=False
                        ))
            else:
                if(not( car.rentals and car.sales)):                                            
                    selected_cars.append(Vehicle(
                        id=car.id,
                        make=car.make,
                        model=car.model,
                        #price=car.price,
                        owner_email=car.owner_email,
                        max_speed=car.max_speed,
                        mileage=car.mileage,
                        average_consumption=car.average_consumption,
                        color=car.color,
                        sales=False,
                        rentals=False
                        ))
        return selected_cars
    
"""def tri_par_para(cars: list[Vehicle],price_max: int=1000000000,mileage :int=1000000000, vitesse_max : int=1000000000):
    new_list=[]
    for car in cars:
        if(car.)""" #vais faire en js directement dans la page

                
        
            
            