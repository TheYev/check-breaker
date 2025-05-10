from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
    username: str = Field(min_length=2, max_length=25)
    email: str = Field(min_length=6, max_length=100)
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
