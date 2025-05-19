from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
    username: str = Field(min_length=2, max_length=25, description="Username (2-25 characters)")
    email: str = Field(min_length=6, max_length=100, description="Email (6-100 characters)")
    password: str = Field(min_length=6, max_length=128, description="Password (6-128 characters)")
    
    model_config = {
        "json_schema_extra": {
            "title": "Request to create a user",
            "description": "Auth model",
            "example": {
                "username": "John",
                "email": "john@gmail.com",
                "password": "password",
            }
        }
    }
    
class Token(BaseModel):
    access_token: str
    token_type: str
