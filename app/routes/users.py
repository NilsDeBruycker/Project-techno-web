import hashlib
from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Request, Form, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.login_manager import login_manager
from app.services.users import (
    get_user_by_username, get_user_by_email, sign_up_user,
    promote_user, demote_user, block_user, unblock_user,
    get_all_users, modify_user, change_password, delete_user_by_email
)
from app.schemas import UserSchema
from pydantic import ValidationError
import app.services.cars as cars_service

router = APIRouter(prefix="/users", tags=["Users"])
templates = Jinja2Templates(directory="templates")

@router.get("/login")
def go_to_login(request: Request):
    return templates.TemplateResponse("login.html", context={'request': request})

@router.post("/login")
def login_route(email: Annotated[str, Form()], password: Annotated[str, Form()]):
    user = get_user_by_email(email)
    if user is None or user.password != hashlib.sha3_256(password.encode()).hexdigest():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad credentials.")
    if user.blocked:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is blocked.")
    
    access_token = login_manager.create_access_token(data={'sub': user.email})
    response = RedirectResponse(url="/cars/", status_code=302)
    response.set_cookie(key=login_manager.cookie_name, value=access_token, httponly=True)
    return response

@router.get("/sign_up")
def go_to_sign_up(request: Request):
    return templates.TemplateResponse("signup.html", context={'request': request})

@router.post("/sign_up")
def sign_up_route(username: Annotated[str, Form()], email: Annotated[str, Form()], password: Annotated[str, Form()], password2: Annotated[str, Form()]):
    if get_user_by_email(email) is not None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Email already in use")
    if password != password2:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Passwords do not match")
    
    new_user = {
        "username": username,
        "email": email,
        "password": hashlib.sha3_256(password.encode()).hexdigest(),
        "role": "normal",
        "blocked": False
    }
    
    try:
        new_user = UserSchema(**new_user)
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials.")
    
    sign_up_user(new_user)
    return RedirectResponse(url="/cars/", status_code=302)

@router.post('/logout')
def logout_route():
    response = RedirectResponse(url="/cars/", status_code=302)
    response.delete_cookie(key=login_manager.cookie_name, httponly=True)
    return response

@router.post("/block")
def block_user_route(email: Annotated[str, Form()], user: UserSchema = Depends(login_manager)):
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only admins can block users.")
    if get_user_by_email(email) is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="User doesn't exist")
    
    block_user(email)
    return RedirectResponse(url="/users/", status_code=302)

@router.post("/unblock")
def unblock_user_route(email: Annotated[str, Form()], user: UserSchema = Depends(login_manager)):
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only admins can unblock users.")
    if get_user_by_email(email) is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="User doesn't exist")
    
    unblock_user(email)
    return RedirectResponse(url="/users/", status_code=302)

@router.get("/me")
def current_user_route(user: UserSchema = Depends(login_manager)):
    return user

@router.get("/")
def show_all_users(request: Request, user: UserSchema = Depends(login_manager)):
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only admins can use this page.")
    
    users = get_all_users()
    return templates.TemplateResponse("manage_users.html", context={'request': request, 'current_user': user, 'users': users})

@router.post("/promote")
def promote_user_route(email: Annotated[str, Form()], current_user: UserSchema = Depends(login_manager)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can promote users.")
    if get_user_by_email(email) is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="User doesn't exist")
    
    promote_user(email)
    return RedirectResponse(url="/users/", status_code=302)

@router.post("/demote")
def demote_user_route(email: Annotated[str, Form()], current_user: UserSchema = Depends(login_manager)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can demote users.")
    if get_user_by_email(email) is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="User doesn't exist")
    
    demote_user(email)
    return RedirectResponse(url="/users/", status_code=302)

@router.get("/profile")
def go_to_profile(request: Request, user: UserSchema = Depends(login_manager)):
    cars = cars_service.get_own_cars(user)
    return templates.TemplateResponse("see_profile.html", context={'request': request, "cars": cars, 'current_user': user})

@router.post("/modify")
def modify_profile(new_username: Annotated[str, Form()], current_user: UserSchema = Depends(login_manager)):
    modify_user(new_username, current_user)
    return RedirectResponse(url="/users/profile", status_code=302)

@router.post("/new_password")
def redo_password(password: Annotated[str, Form()], password2: Annotated[str, Form()], user: UserSchema = Depends(login_manager)):
    if password != password2:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Passwords do not match")
    
    change_password(user.email, hashlib.sha3_256(password.encode()).hexdigest())
    return RedirectResponse(url="/users/profile", status_code=302)

@router.post("/delete")
def delete_user(email: Annotated[str, Form()], user: UserSchema = Depends(login_manager)):
    if get_user_by_email(email) is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="User doesn't exist")
    
    delete_user_by_email(email)
    return RedirectResponse(url="/users/", status_code=302)
