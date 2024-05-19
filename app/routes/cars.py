from uuid import uuid4
from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Form, Depends
from fastapi.responses import RedirectResponse
from pydantic import ValidationError
from app.schemas import cars, UserSchema # Assuming you have a Car and UserSchema schema
import app.services.cars as service  # Assuming you have a service module for cars
from app.login_manager import login_manager
from fastapi.templating import Jinja2Templates
from fastapi import Request
from app.services.users import get_user_by_email

router = APIRouter(prefix="/cars", tags=["Cars"])
templates = Jinja2Templates(directory="templates")

@router.get('/')
def get_all_cars(request: Request, user: UserSchema = Depends(login_manager.optional)):
    if user is not None:
        if user.role == "admin":
            cars = service.get_all_cars()
        else:
            cars = service.get_public_cars()
            cars_self = service.get_own_cars(user)
            cars = cars + cars_self
    else:
        cars = service.get_public_cars()
    return templates.TemplateResponse(
        "all_cars.html",
        context={'request': request, 'current_user': user, 'cars': cars}
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
    elif user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only admins can use this page"
        )
    return templates.TemplateResponse(
        "new_car.html",
        context={'request': request}
    )

@router.post('/new')
def create_new_car(make: Annotated[str, Form()], model: Annotated[str, Form()], year: Annotated[int, Form()], owner: Annotated[str, Form()] = None):
    if owner is not None:
        if get_user_by_email(owner) is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No owner with this email"
            )
    new_car_data = {
        "id": str(uuid4()),
        "make": make,
        "model": model,
        "year": year,
        "owner": owner,
    }
    try:
        new_car_test = cars(**new_car_data)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid make, model, or year for the car.",
        )
    service.save_car(new_car_test)
    return RedirectResponse(url="/cars/", status_code=302)

@router.post('/modify')
def modify_car(id: Annotated[str, Form()], make: Annotated[str, Form()], model: Annotated[str, Form()], year: Annotated[int, Form()], owner: Annotated[str, Form()] = None):
    if not service.is_car_exist(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car ID not found"
        )
    if owner is not None:
        if get_user_by_email(owner) is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No owner with this email"
            )
    new_car_data = {
        "id": id,
        "make": make,
        "model": model,
        "year": year,
        "owner": owner,
    }
    try:
        new_car_test = cars(**new_car_data)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid make, model, or year for the car.",
        )
    service.modify_car_by_id(id, new_car_data)
    return RedirectResponse(url="/cars/", status_code=302)

@router.post('/delete')
def delete_car(id: Annotated[str, Form()]):
    if not service.is_car_exist(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car ID not found"
        )
    service.delete_car_by_id(id)
    return RedirectResponse(url="/cars/", status_code=302)

@router.post('/sell')
def sell_car(id: Annotated[str, Form()], user: UserSchema = Depends(login_manager)):
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
    if car.status == "en vente":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This car is already listed for sale."
        )
    modified_car = car.copy(update={"status": "en vente"})
    service.modify_car_by_id(car.id, modified_car)
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
    return RedirectResponse(url="/users/profile", status_code=302)

@router.post('/buy')
def buy_car(id: Annotated[str, Form()], user: UserSchema = Depends(login_manager)):
    car = service.get_car_by_id(id)
    if car is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )
    if car.status != "en vente":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This car is not listed for sale."
        )
    modified_car = car.copy(update={"owner": user.email, "status": "privé"})
    service.modify_car_by_id(car.id, modified_car)
    return RedirectResponse(url="/cars/", status_code=302)

@router.post("/change_owner")
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
    return RedirectResponse(url="/cars/", status_code=302)

@router.post('/rent')
def rent_car(id: Annotated[str, Form()], user: UserSchema = Depends(login_manager)):
    car = service.get_car_by_id(id)
    if car is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )
    if car.status != "privé":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This car is not available for rent."
        )
    modified_car = car.copy(update={"status": "en location"})
    service.modify_car_by_id(car.id, modified_car)
    return RedirectResponse(url="/cars/", status_code=302)
