from app.schemas import UserSchema
from app.database import Session
from app.models.car import User  
from sqlalchemy import select


def get_user_by_username(username: str):
    with Session() as session:
        statement = select(User).filter(User.username==username)
        user = session.scalars(statement).one()
        if user is not None:
            return UserSchema(
                username=user.username,
                email=user.email,
                password=user.password,
                role=user.role,
                blocked=user.blocked,
            )
    return None


def get_user_by_email(email: str):
    with Session() as session:
        statement = select(User).filter(User.email==email)
        user = session.scalar(statement) 
        if user is not None:
            return UserSchema(
                email=user.email,
                username=user.username,
                password=user.password,
                role=user.role,
                blocked=user.blocked,
            )
    return None


def sign_up_user(new_user:UserSchema):
    with Session() as session:
       new_user_instance= User(
                email=new_user.email,
                username=new_user.username,
                password=new_user.password,
                role=new_user.role,
                blocked=new_user.blocked,)
       session.add(new_user_instance)
       session.commit()
    return new_user



def get_all_users() :
    with Session() as session:
        statement = select(User)
        users_data = session.scalars(statement).unique().all()
        return [
            User(
                email=user.email,
                password=user.password,
                username=user.username,
                role=user.role,
                blocked=user.blocked,
            )     
            
            for user in users_data
        ]



def block_user(email: str):
    with Session() as session:
        user = session.query(User).filter(User.email == email).first()
        if user is not None:
            user.blocked = True
            session.commit()


def unblock_user(email: str):
    with Session() as session:
        user = session.query(User).filter(User.email == email).first()
        if user is not None:
            user.blocked = False
            session.commit()


def promote_user(email: str) -> User:
    with Session() as session:    
        user = session.query(User).filter(User.email == email).first()
        if user is not None:
            user.role = "admin"
            session.commit()

    return user


def demote_user(email: str) -> User:
    with Session() as session:
        user = session.query(User).filter(User.email == email).first()
        if user:
            user.role = "normal"
            session.commit()

    return user

def delete_user_by_email( email: str):
    with Session() as session:
        statement = select(User).filter(User.email==email)
        user = session.execute(statement).scalar_one()
        session.delete(user)
        session.commit()

def modify_user(new_username,curent_user:User):
     with Session() as session:
        statement = select(User).filter(User.email==curent_user.email)
        user = session.scalars(statement).one()
        user.username=new_username
        session.commit()

def change_password(email,new_pasword):
    with Session() as session:
        statement = select(User).filter(User.email==email)
        user = session.scalars(statement).one()
        user.password=new_pasword
        session.commit()
