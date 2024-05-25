from uuid import uuid4
from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Form, Depends
from fastapi.responses import RedirectResponse
from pydantic import ValidationError
from app.schemas.cars import Car # Assuming you have a Car and UserSchema schema
from app.schemas.UserSchema import UserSchema
import app.services.cars as service  # Assuming you have a service module for cars
from app.login_manager import login_manager
from fastapi.templating import Jinja2Templates
from fastapi import Request
from app.services.users import get_user_by_email

router = APIRouter(prefix="/cars", tags=["Cars"])
templates = Jinja2Templates(directory="templates")

@router.get('/')
def get_all_cars(request: Request, user: UserSchema = Depends(login_manager.optional)):
    return templates.TemplateResponse(
            "front_page.html",
            context={'request': request}
    )

@router.get('/new')
def get_car(request: Request, user: UserSchema = Depends(login_manager)):
    if user is None:
        return templates.TemplateResponse(
            "login.html",
            context={'request': request}
        )
    elif user.blocked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are blocked."
        )
    elif user.role != "vendeur":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="seul les vendeurs peuvent utiliser cette page"
        )
    return templates.TemplateResponse(
        "new_car.html",
        context={'request': request}
    )

@router.post('/new')
def create_new_car(make: Annotated[str, Form()], model: Annotated[str, Form()],color:Annotated[str,Form()],max_speed: Annotated[int,Form()], mileage: Annotated[int, Form()],average_consumption: Annotated[int,Form()],user: UserSchema = Depends(login_manager),price_sell:Annotated[float, Form()]=0,price_rent: Annotated[float,Form()]=0):
    if price_sell==0 and price_rent==0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="please input a price for rent or sell",
        )
    new_car_data = {
        "id": str(uuid4()),
        "brand": make,
        "model": model,
        "color": color,
        "max_speed": max_speed,
        "mileage": mileage,
        "average_consumption": average_consumption,
        "price_sell": price_sell,
        "price_rent": price_rent,
        "owner_email": user.email,
        "sell":True,
        "rent":True
        
    }
    try:
        new_car_test = Car(**new_car_data)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid make, model, or other for the car.",
        )
    service.save_car(new_car_test)
    return RedirectResponse(url="/cars/", status_code=302)

@router.post('/modify')
def modify_car(id: Annotated[str, Form()],make: Annotated[str, Form()], model: Annotated[str, Form()],color:Annotated[str,Form()],max_speed: Annotated[int,Form()], mileage: Annotated[int, Form()],average_consumption: Annotated[int,Form()],user: UserSchema = Depends(login_manager),price_sell:Annotated[float, Form()]=0,price_rent: Annotated[float,Form()]=0):
    if not service.is_car_exist(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car ID not found"
        )
    if user.seller!=True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="only seller can modify cars")
    new_car_data = {
        "id": id,
        "brand": make, #supr?
        "model": model, #supr?
        "color": color, #supr?
        "max_speed": max_speed, #supr?
        "mileage": mileage,
        "average_consumption": average_consumption, #supr?
        "price_sell": price_sell,
        "price_rent": price_rent,
        "owner_email": user.email, 
        "sell":(price_sell!=0),
        "rent":(price_rent!=0),
    }
    try:
        new_car_test = Car(**new_car_data)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid make, model, or year for the car.",
        )
    service.modify_car_by_id(id, new_car_data)
    return RedirectResponse(url="/cars/", status_code=302)

@router.post('/delete')
def deletecar(id: Annotated[str, Form()], user: UserSchema = Depends(login_manager.optional)):
    if user is None:
            return RedirectResponse(url="/users/login", status_code=302)

    elif user.blocked==True:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="blocked."
        )
    elif user.role!="admin" or user.seller!=True:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="only admins and sellers can use this page"
        )
   
    if not service.is_car_exist(id):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
                detail=" id not found"
        )
    car_to_delete=service.get_car_by_id(id)
    if car_to_delete.owner_email!=user.email or car_to_delete.rent_owner_email:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you cannot delete a car that is rented or not yours"
        )
    service.delete_car_by_id(id)
    return RedirectResponse(url="/cars/", status_code=302)

"""@router.post('/sell')
def sell_car(id: Annotated[str, Form()], user: UserSchema = Depends(login_manager)):
    car = service.get_car_by_id(id)
    if car is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )
    if user.email != car.owner_email and user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not the owner of this car."
        )
    if car.sell == True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This car is already listed for sale."
        )
    elif car.rent_owner_email is not None:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This car is already rented by someone else."
        )
    service.sell_car(car.id, modified_car)
    return RedirectResponse(url="/users/profile", status_code=302)"""
"""@router.post('/sell')
def sell_book(id: Annotated[str, Form()],user: UserSchema = Depends(login_manager)):
    book=service.get_book_by_id(id)
    if book is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
                detail=" book not found"
        )
    if user.email!=book.owner_email and user.role!="admin":
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="that book is not yours."
        )
    elif book.status=="en vente":
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="already selling this book"
        )
    else:
        modified_book={
            "Author":book.Author,
            "Editor":book.Editor,
            "id":book.id,
            "name":book.name,
            "Prix":book.Prix,
            "Owner":book.owner_email,
            "status":"en vente",
        }
        service.modify_book_by_id(book.id,modified_book)
        return RedirectResponse(url="/users/profile", status_code=302)
@router.post('/unsell')
def retire_car_from_sale(id: Annotated[str, Form()], user: UserSchema = Depends(login_manager)):
    car = service.get_car_by_id(id)
    if car is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )
    if user.email != car.owner and user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not the owner of this car."
        )
    if car.status == "privé":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This car is already private."
        )
    modified_car = car.copy(update={"status": "privé"})
    service.modify_car_by_id(car.id, modified_car)
    return RedirectResponse(url="/users/profile", status_code=302)"""

@router.post('/buy')
def buy_car(id: Annotated[str, Form()], user: UserSchema = Depends(login_manager)):
    car = service.get_car_by_id(id)
    if car is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )
    if car.sell !=True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This car is not listed for sale."
        )
    elif car.rent_owner_email is not None:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you buy a car that is rented"
        )
    new_car_data = {
        "id": id,
        "brand": car.make, #supr?
        "model": car.model, #supr?
        "color": car.color, #supr?
        "max_speed": car.max_speed, #supr?
        "mileage": car.mileage,
        "average_consumption": car.average_consumption, #supr?
        "price_sell": 0,
        "price_rent": 0,
        "owner_email": user.email, 
        "sell":False,
        "rent":False,
    }
    service.modify_car_by_id(car.id,new_car_data)
    return RedirectResponse(url="/cars/", status_code=302)

@router.post('/rent')
def buy_car(id: Annotated[str, Form()], user: UserSchema = Depends(login_manager)):
    car = service.get_car_by_id(id)
    if car is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )
    if car.rent !=True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This car is not listed for rent."
        )
    elif car.rent_owner_email is not None:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you rent a car that is already rented"
        )
    if user.seller==True:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="only admins and buyers can use this page"
        )
    new_car_data = {
        "id": id,
        "brand": car.make, #supr?
        "model": car.model, #supr?
        "color": car.color, #supr?
        "max_speed": car.max_speed, #supr?
        "mileage": car.mileage,
        "average_consumption": car.average_consumption, #supr?
        "price_sell": car.sell,
        "price_rent": car.rent,
        "owner_email": user.email, 
        "sell":car.sell,
        "rent":False,
        "rent_owner_email":user.email
    }
    try:
        new_car_test = Car(**new_car_data)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid make, model, or year for the car.",
        )
    service.modify_car_by_id(car.id,new_car_data,True)
    return RedirectResponse(url="/cars/", status_code=302)
"""@router.post("/change_owner")
def change_car_owner(id: Annotated[str, Form()], new_owner: Annotated[str, Form()], user: UserSchema = Depends(login_manager)):
    car = service.get_car_by_id(id)
    if car is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )
    if user.role != "admin" and user.email != car.owner:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to change the owner of this car."
        )
    if get_user_by_email(new_owner) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No user with this email exists."
        )
    modified_car = car.copy(update={"owner": new_owner})
    service.modify_car_by_id(car.id, modified_car)
    return RedirectResponse(url="/cars/", status_code=302)"""

@router.post('/unrent')
def rent_car(id: Annotated[str, Form()], user: UserSchema = Depends(login_manager)):
    car = service.get_car_by_id(id)
    if car is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )
    if car.rent_owner_email is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This car is not rented."
        )
    if car.rent_owner_email != user.email:
     raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This car is not rented by you."
        ) 
    new_car_data = {
        "id": id,
        "brand": car.make, #supr?
        "model": car.model, #supr?
        "color": car.color, #supr?
        "max_speed": car.max_speed, #supr?
        "mileage": car.mileage,
        "average_consumption": car.average_consumption, #supr?
        "price_sell": car.sell,
        "price_rent": car.rent,
        "owner_email": user.email, 
        "sell":car.sell,
        "rent":True,
        "rent_owner_email": None
    }
    try:
        new_car_test = Car(**new_car_data)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid make, model, or year for the car.",
        )
    service.modify_car_by_id(car.id, new_car_data,True)
    return RedirectResponse(url="/cars/", status_code=302)


@router.post('/search')
def search(search_therm: Annotated[str,Form()]):
    service.search(search_therm)
