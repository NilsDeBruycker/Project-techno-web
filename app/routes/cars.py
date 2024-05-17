from uuid import uuid4
from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Form, Depends
from fastapi.responses import RedirectResponse
from pydantic import ValidationError
from app.schemas import Car  # Assuming you have a Car schema
import app.services.cars as service  # Assuming you have a service module for cars
from app.login_manager import login_manager
from app.schemas import UserSchema
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
def get_car(request: Request, user: UserSchema = Depends(login_manager.optional)):
    if user == None:
        return templates.TemplateResponse(
            "login.html",
            context={'request': request, }
        )
    elif user.blocked == True:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="blocked."
        )
    elif user.role != "admin":
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="only admins can use this page"
        )
    return templates.TemplateResponse(
        "new_car.html",
        context={'request': request, }
    )


@router.post('/new')
def create_new_car(make: Annotated[str, Form()], model: Annotated[str, Form()], year: Annotated[int, Form()], owner: Annotated[str, Form()] = None):
    if owner is not None:
        if get_user_by_email(owner) is None:
            return HTTPException(
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
        new_car_test = Car.model_validate(new_car_data)
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
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=" id not found"
        )
    if owner is not None:
        if get_user_by_email(owner) is None:
            return HTTPException(
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
        new_car_test = Car.model_validate(new_car_data)
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
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=" id not found"
        )
    service.delete_car_by_id(id)
    return RedirectResponse(url="/cars/", status_code=302)

@router.post('/sell')
def sell_car(id: Annotated[str, Form()], user: UserSchema = Depends(login_manager)):
    car = service.get_car_by_id(id)
    if car is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )
    if user.email != car.owner_email and user.role != "admin":
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not the owner of this car."
        )
    elif car.status == "en vente":
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This car is already listed for sale."
        )
    else:
        modified_car = {
            "make": car.make,
            "model": car.model,
            "id": car.id,
            "year": car.year,
            "owner": car.owner_email,
            "status": "en vente",
        }
        service.modify_car_by_id(car.id, modified_car)
        return RedirectResponse(url="/users/profile", status_code=302)


@router.post('/unsell')
def retire_car_from_sale(id: Annotated[str, Form()], user: UserSchema = Depends(login_manager)):
    car = service.get_car_by_id(id)
    if car is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )
    if user.email != car.owner_email and user.role != "admin":
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not the owner of this car."
        )
    elif car.status == "privé":
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This car is already private."
        )
    else:
        modified_car = {
            "make": car.make,
            "model": car.model,
            "id": car.id,
            "year": car.year,
            "owner": car.owner_email,
            "status": "privé",
        }
        service.modify_car_by_id(car.id, modified_car)
        return RedirectResponse(url="/users/profile", status_code=302)


@router.post('/buy')
def buy_car(id: Annotated[str, Form()], user: UserSchema = Depends(login_manager)):
    car = service.get_car_by_id(id)
    if car is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )
    if car.status != "en vente":
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This car is not listed for sale."
        )
    else:
        modified_car = {
            "make": car.make,
            "model": car.model,
            "id": car.id,
            "year": car.year,
            "owner": user.email,
            "status": "privé",
        }
        service.modify_car_by_id(car.id, modified_car)
        return RedirectResponse(url="/cars/", status_code=302)


@router.post("/change_owner")
def change_car_owner(id: Annotated[str, Form()], new_owner: Annotated[str, Form()], user: UserSchema = Depends(login_manager)):
    car = service.get_car_by_id(id)
    if car is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )
    if user.role != "admin" and user.email != car.owner_email:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to change the owner of this car."
        )
    if get_user_by_email(new_owner) is None:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No user with this email exists."
        )
    modified_car = {
        "make": car.make,
        "model": car.model,
        "id": car.id,
        "year": car.year,
        "owner": new_owner,
        "status": car.status,
    }
    service.modify_car_by_id(car.id, modified_car)
    return RedirectResponse(url="/cars/", status_code=302)
