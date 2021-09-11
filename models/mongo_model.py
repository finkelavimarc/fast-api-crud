from pydantic import BaseModel
from bson.objectid import ObjectId

from typing import Optional


class UserRegister(BaseModel):
    name: str
    username: str
    email: str
    password: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class Token(BaseModel):
    access_token: Optional[str] = None
    token_type: Optional[str] = None


class TokenData(BaseModel):
    username: Optional[str] = None


class ExtractToken(BaseModel):
    sub: str
    exp: str
