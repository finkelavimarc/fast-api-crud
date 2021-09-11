from jose import jwt, JWTError
from auth.crypto_context import CryptoContext
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from typing import Optional
from models.mongo_model import TokenData, User, ExtractToken
from decouple import config
from fastapi.security import OAuth2PasswordBearer
from mongo.db_crud import Mongo

SECRET_KEY = config("secret_key")
ALGORITHM = config("algorithm")
ACCESS_TOKEN_EXPIRE_MINUTES = int(config("access_token_expire_minutes"))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await Middleware._get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


class Middleware:
    db = Mongo()

    def __init__(self):
        self.crypto_context = CryptoContext()

    async def _authenticate_user(self, username: str, password: str):
        user = await self._get_user(username)
        if not user:
            return False
        if not self.crypto_context.verify_password(password, user["password"]):
            return False
        return user

    def _create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    async def _get_user(username: str):
        user = await Middleware.db.get_user(username)
        return user

    async def login_handle(self, username, plain_password) -> dict:
        try:
            user = await self._authenticate_user(username, plain_password)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = self._create_access_token(
                data={"sub": user["username"]}, expires_delta=access_token_expires
            )
            return {"access_token": access_token, "token_type": "bearer"}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"{e}",
            )

    def decode_jwt_token(self, token: str = Depends(oauth2_scheme)):
        res = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return ExtractToken(**res)

    async def get_current_active_user(
        self, current_user: User = Depends(get_current_user)
    ):
        if not current_user:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
