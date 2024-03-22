from typing import Optional
from pydantic import BaseModel
from bson.objectid import ObjectId

class UserRegister(BaseModel):
    """
    Model for registering a user.
    """
    name: str
    username: str
    email: str
    password: str

    class Config:
        """
        Pydantic configuration options.
        """
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class User(BaseModel):
    """
    Model representing a user.
    """
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class Token(BaseModel):
    """
    Model representing an access token.
    """
    access_token: Optional[str] = None
    token_type: Optional[str] = None

class TokenData(BaseModel):
    """
    Model representing token data.
    """
    username: Optional[str] = None

class ExtractToken(BaseModel):
    """
    Model representing extracted token data.
    """
    sub: str
    exp: str
