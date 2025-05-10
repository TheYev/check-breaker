from fastapi import Depends, HTTPException
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from jose import jwt
from passlib.context import CryptContext
from typing import Union
from datetime import datetime, timezone, timedelta

from ..schemas.auth import CreateUserRequest
from ..utils.config import settings
from ..utils.depends import db_dependency
from ..models.models import Users


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

SECRET_KEY = settings.SECRET_KEY
ALGORITM = settings.ALGORITM
ACCESS_TOKEN_EPIRE_MINUTES = int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)

def authenticate_user(username: str, password: str, db: db_dependency) -> Union[Users, bool]:
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_key(username: str, email: str, user_id: int):
    encode = {'sub': username, 'id': user_id, 'email': email}
    expires = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EPIRE_MINUTES)
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, ALGORITM)

def create_user_model(create_user_request: CreateUserRequest, db: db_dependency) -> Users:
    create_user = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        update_at = datetime.now(timezone.utc)
    )
    db.add(create_user)
    db.commit()
    db.refresh(create_user)
    return create_user

def login_access_token(form_date: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_date.username, form_date.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")
    
    token = create_access_key(user.username, user.email, user.id)
    
    return {'access_token': token, 'token_type': 'bearer'}
