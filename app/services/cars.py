from uuid import uuid4
from sqlalchemy import select, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Session
from app.models.car import Vehicle
from app.schemas.cars import Car as CarSchema
from app.schemas.cars import Rental as RentalSchema
from app.schemas.UserSchema import UserSchema

# Function to save a new rental
"""def save_rental(new_rental: RentalSchema):
    with Session() as session:
        rental_entity = Rental(
            user_email=new_rental.user_email,
            car_id=new_rental.car_id
        )
        session.add(rental_entity)
        session.commit()"""

""""def sell_car(id : str,):
    with Session() as session:
        statement = select(Vehicle).filter(Vehicle.id == id)

        

        car = session.scalars(statement).one()
        car.sell=True"""
# Function to save a new car
def save_car(new_car: CarSchema):
    
    with Session() as session:
        new_car_entity = Vehicle(
            id=new_car.id,
            make=new_car.brand,
            model=new_car.model,
            price_sell=new_car.price_sell,
            price_rent=new_car.price_rent,
            owner_email=new_car.owner_email,
            sell=new_car.sell,
            rent=new_car.rent,
            max_speed=new_car.max_speed,
            color=new_car.color,
            mileage=new_car.mileage,
            average_consumption=new_car.average_consumption

        )
        session.add(new_car_entity)
        session.commit()

# Function to get all public cars remplacer par search
"""def get_public_cars():
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
"""
# Function to get all cars owned by a user
def get_own_cars(user:UserSchema):
    with Session() as session:
        statement = select(Vehicle).filter(Vehicle.owner_email == user.email)
        cars_data = session.scalars(statement).unique().all()
    return [
        Vehicle(
            id=car.id,
            make=car.make,
            model=car.model,
            #price=car.price,
            price_sell= car.price_sell,
            price_rent=car.price_rent,
            owner_email=car.owner_email,
            max_speed=car.max_speed,
            mileage=car.mileage,
            average_consumption=car.average_consumption,
            color=car.color,
            sell=car.sell,
            rent=car.rent,
            rent_owner_email=car.rent_owner_email
        )
        for car in cars_data
    ]

# Function to get all cars
def get_all_cars() -> list[Vehicle]:
    with Session() as session:
        statement = select(Vehicle)
        cars_data = session.scalars(statement).unique().all()
    return [
       Vehicle(
            id=car.id,
            make=car.make,
            model=car.model,
            #price=car.price,
            price_sell= car.price_sell,
            price_rent=car.price_rent,
            owner_email=car.owner_email,
            max_speed=car.max_speed,
            mileage=car.mileage,
            average_consumption=car.average_consumption,
            color=car.color,
            sell=car.sell,
            rent=car.rent,
            rent_owner_email=car.rent_owner_email
            )
        for car in cars_data
    ]

# Function to delete a car by its ID
def delete_car_by_id(car_id: str):
    with Session() as session:
        statement = select(Vehicle).filter(Vehicle.id == car_id)
        car = session.scalars(statement).one()
        session.delete(car)
        session.commit()

# Function to check if a car exists by its ID
def is_car_exist(car_id: str):
    with Session() as session:
        statement = select(Vehicle).filter(Vehicle.id == car_id)
        car = session.scalar(statement)
        return car is not None

# Function to get a car by its ID
def get_car_by_id(car_id):
    with Session() as session:
        statement = select(Vehicle).filter(Vehicle.id == car_id)
        car = session.scalars(statement).one()
        if car:
            return Vehicle(
                id=car.id,
                make=car.make,
                model=car.model,
                #price=car.price,
                price_sell= car.price_sell,
                price_rent=car.price_rent,
                owner_email=car.owner_email,
                max_speed=car.max_speed,
                mileage=car.mileage,
                average_consumption=car.average_consumption,
                color=car.color,
                sell=car.sell,
                rent=car.rent,
                rent_owner_email=car.rent_owner_email
            )

# Function to modify a car by its ID not needed ferai si temp
def modify_car_by_id(car_id: str, modified_car :dict,transaction : bool=False) -> None:
    with Session() as session:
        statement = select(Vehicle).filter(Vehicle.id == car_id)
        

        car = session.scalars(statement).one()
        if car:
            car.owner_email = modified_car["owner_email"]
            car.make = modified_car["brand"] 
            car.model = modified_car["model"]
            car.max_speed = modified_car["max_speed"]
            car.mileage = modified_car["mileage"]
            car.average_consumption = modified_car["average_consumption"]
            car.color = modified_car["color"]
            car.price_sell = modified_car["price_sell"]
            car.price_rent = modified_car["price_rent"]
            car.sell = modified_car["sell"]
            car.rent = modified_car["rent"]
            if transaction:
                car.rent_owner_email=modified_car["rent_owner_email"]
            session.commit()
            return car
        return None
        id: int
    model: str
    brand: str
    color: str
    max_speed: int
    mileage: int
    average_consumption: float
    price_sell: float
    price_rent: float
    rented: bool
    sold:bool
    owner_email: str


# Function to rent a car
"""def rent_car(user_email: str, car_id: str):
    with Session() as session:
        car = session.query(cars).filter(cars.id == car_id, cars.status == "available").one_or_none()
        if car:
            rental = Rental(user_email=user_email, car_id=car_id)
            session.add(rental)
            car.status = "rented"
            session.commit()
            return True
        return False"""

# Function to return a rented car
"""def return_car(user_email: str, car_id: str):
    with Session() as session:
        rental = session.query(Rental).filter(Rental.user_email == user_email, Rental.car_id == car_id).one_or_none()
        if rental:
            car = session.query(cars).filter(cars.id == car_id).one()
            car.status = "available"
            session.delete(rental)
            session.commit()
            return True
        return False"""

# Function to get all cars rented by a user
def get_rented_cars(user: UserSchema):
    with Session() as session:
        if user.seller==False:
            statement = select(Vehicle).filter(Vehicle.rent_owner_email == user.email)
            cars_data = session.scalars(statement).all()
        else:
            statement = select(Vehicle).filter(Vehicle.owner_email == user.email,Vehicle.rent_owner_email!=user.email)
            cars_data = session.scalars(statement).all()
    return [
        Vehicle(
            id=car.id,
            make=car.make,
            model=car.model,
            price_sell=car.price_sell,
            price_rent=car.price_rent,

            owner_email=car.owner_email,
            max_speed=car.max_speed,
            mileage=car.mileage,
            average_consumption=car.average_consumption,
            color=car.color,
            sell=car.sell ,
            rent=car.rent,
            rent_owner_email=car.rent_owner_email
        )
        for car in cars_data
    ]
#Function search of 
def search(search_therm: str,price_sell_max: int=1000000000,price_rent_max: int=1000000000,mileage :int=1000000000, vitesse_max : int=1000000000,conso_max=200):
    with Session() as session:
        statement=select(Vehicle)
        cars = session.scalars(statement).all()
        selected_cars=[]
        for car in cars:
            if (search_therm!=''):
                if((car.make==search_therm or
                    search_therm==car.model or
                    search_therm==car.color)
                    and ( car.rent or car.sell) and(car.price_rent<price_rent_max and car.price_sell<price_sell_max and car.max_speed<vitesse_max and  car.mileage<mileage and car.average_consumption<conso_max)):

                    
                
                    selected_cars.append(Vehicle(
                        id=car.id,
                        make=car.make,
                        model=car.model,
                        #price=car.price,
                        price_sell= car.price_sell,
                        price_rent=car.price_rent,
                        owner_email=car.owner_email,
                        max_speed=car.max_speed,
                        mileage=car.mileage,
                        average_consumption=car.average_consumption,
                        color=car.color,
                        sell=car.sell,
                        rent=car.rent,
                        rent_owner_email=car.rent_owner_email
                        ))
            else:
                if(( car.sell or car.rent)and(car.price_rent<price_rent_max and car.price_sell<price_sell_max and car.max_speed<vitesse_max and  car.mileage<mileage and car.average_consumption<conso_max)):                                            
                    selected_cars.append(Vehicle(
                        id=car.id,
                        make=car.make,
                        model=car.model,
                        price_sell= car.price_sell,
                        price_rent=car.price_rent,
                        owner_email=car.owner_email,
                        max_speed=car.max_speed,
                        mileage=car.mileage,
                        average_consumption=car.average_consumption,
                        color=car.color,
                        sell=car.sell,
                        rent=car.rent,
                        rent_owner_email=car.rent_owner_email
                        ))
        return selected_cars
    
"""def tri_par_para(cars: list[Vehicle],price_max: int=1000000000,mileage :int=1000000000, vitesse_max : int=1000000000):
    new_list=[]
    for car in cars:
        if(car.)""" #vais faire en js directement dans la page

                
        
            
            