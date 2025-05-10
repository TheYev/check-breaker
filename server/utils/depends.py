from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from starlette import status

from sqlalchemy.orm import Session

from typing import Annotated, AsyncIterator

from jose import jwt, JWTError

from ..utils.config import settings
from ..utils.database import SessionLocal


SECRET_KEY = settings.SECRET_KEY
ALGORITM = settings.ALGORITM

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITM])
        username: str = payload.get('sub')
        email: str = payload.get('email')
        user_id: int = payload.get('id')
        if username is None or email is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")
        return {'id': user_id, 'username': username, 'email': email}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")
        
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]