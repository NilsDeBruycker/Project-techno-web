import hashlib
from typing import Annotated
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import APIRouter, HTTPException, status, Request, Form, Depends, Body
from app.login_manager import login_manager
from app.services.users import get_user_by_username,sign_up_user,promote_user,demote_user
from app.schemas import UserSchema
from pydantic import ValidationError
from fastapi.templating import Jinja2Templates
router = APIRouter(prefix="/users")
templates = Jinja2Templates(directory="templates")
import app.services.users as user_service
import app.services.cars as books_service
@router.get("/login")
def go_tosignup(request:Request):    
    return templates.TemplateResponse(
        "login.html",
        context={'request': request}
    )

@router.post("/login")
def login_route(
        email:Annotated[str, Form()],
        password: Annotated[str, Form()],
):
    user = user_service.get_user_by_email(email)
    if user is None or user.password!= hashlib.sha3_256(password.encode()).hexdigest():
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bad credentials."
        )
    if user.blocked==True:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="blocked."
            )
    access_token = login_manager.create_access_token(
        data={'sub': user.email}
    )
    
    response = RedirectResponse(url="/books/", status_code=302)
    response.set_cookie(
        key=login_manager.cookie_name,
        value=access_token,
        httponly=True
    )
    return response

@router.get("/sign_up")
def go_tosignup(request:Request):    
    return templates.TemplateResponse(
        "signup.html",
        context={'request': request}
    )

@router.post("/sign_up")
def sign_up_route(username: Annotated[str, Form()],email:Annotated[str, Form()],password: Annotated[str, Form()],password2: Annotated[str, Form()]):
    if user_service.get_user_by_email(email) is not None:
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="email already in use")
    
    elif password==password2:
        password=password.encode()
        new_user = {
            "username": username,
            "email": email,
            "password": hashlib.sha3_256(password).hexdigest(),
            "role":"normal",
            "blocked":False}
        
        try:
            new_user = UserSchema.model_validate(new_user)
        except ValidationError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid credential.",
            )
        sign_up_user(new_user)

        return RedirectResponse(url="/books/", status_code=302)
    else:
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="confirmation password is not the same password"
        )

@router.post('/logout')
def logout_route():
    response = RedirectResponse(url="/books/", status_code=302)
    response.delete_cookie(
        key=login_manager.cookie_name,
        httponly=True
    )
    return response

@router.post("/block")
def go_to_block_page(email:Annotated[str, Form()],user: UserSchema = Depends(login_manager),):
    if user_service.get_user_by_email(email) is None:
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="user doesn't exist")
    
    user_service.block_user(email)
    return RedirectResponse(url="/users/", status_code=302)

@router.post("/unblock")
def go_to_block_page(email:Annotated[str, Form()],user: UserSchema = Depends(login_manager),):
    if user_service.get_user_by_email(email) is None:
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="user doesn't exist")
    
    user_service.unblock_user(email)
    return RedirectResponse(url="/users/", status_code=302)


@router.get("/me")
def current_user_route(
    user: UserSchema = Depends(login_manager), #depends renvoie ereure si pas conecté
):
    return user

@router.get("/")
def show_all_users(request:Request,user: UserSchema = Depends(login_manager)):
    users = user_service.get_all_users()
    if user.role!="admin":
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="only admins can use this page"
        )
    return templates.TemplateResponse(
        "manage_users.html",
        context={'request': request,'current_user': user ,'users': users}
        )
@router.post("/promote")
def promote_user_route(email:Annotated[str, Form()], current_user: UserSchema = Depends(login_manager)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can promote users.")
    
    if user_service.get_user_by_email(email) is None:
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="user doesn't exist")
    
    promote_user(email)
    return RedirectResponse(url="/users/", status_code=302)

@router.post("/demote")
def demote_user_route(email:Annotated[str, Form()], current_user: UserSchema = Depends(login_manager)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can demote users.")
    
    if user_service.get_user_by_email(email) is None:
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="user doesn't exist")
    
    demote_user(email)
    return RedirectResponse(url="/users/", status_code=302)

@router.get("/profile")
def go_to_profile(request:Request,user: UserSchema = Depends(login_manager)):
    Books=books_service.get_own_books(user)
    return templates.TemplateResponse(
        "see_profile.html",
        context={'request': request,"books":Books,'current_user': user}
        )

@router.post("/modify")
def modify_profile(new_username:Annotated[str, Form()], current_user: UserSchema = Depends(login_manager)):
    user_service.modify_user(new_username,current_user)
    return RedirectResponse(url="/users/profile", status_code=302)


@router.post("/new_password")
def redo_password(password: Annotated[str, Form()],password2: Annotated[str, Form()],user: UserSchema = Depends(login_manager)):
    if password==password2:
        user_service.change_password(user.email ,hashlib.sha3_256(password.encode()).hexdigest())
    return RedirectResponse(url="/users/profile", status_code=302)

@router.post("/delete")
def delete_user(email: Annotated[str, Form()],user: UserSchema = Depends(login_manager)):
    if user_service.get_user_by_email(email) is None:
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="user doesn't exist")
    user_service.delete_user_by_email(email)
    return RedirectResponse(url="/users/", status_code=302)
