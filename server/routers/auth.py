from fastapi import APIRouter, Depends
from passlib.context import CryptContext
from starlette import status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

from ..utils.depends import db_dependency

from ..schemas.auth import CreateUserRequest, Token

from ..services.auth import create_user_model, login_access_token


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest, db: db_dependency):
    user = create_user_model(create_user_request, db)
    return user
            
@router.post('/token', response_model=Token, status_code=status.HTTP_200_OK)
async def login_for_access_token(form_date: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    token = login_access_token(form_date, db)
    return token
