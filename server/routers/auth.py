from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from starlette import status
from ..utils.database import SessionLocal
from ..models.models import Users
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime, timezone 


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.get("/get")
async def get_some():
    return {"Test:": "Test"}

