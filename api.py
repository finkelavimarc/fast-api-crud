from fastapi import FastAPI, Depends, Request
from models.mongo_model import UserRegister, Token, User
from fastapi.security import OAuth2PasswordRequestForm
from mongo.db_crud import Mongo
from auth.crypto_context import CryptoContext
from src.util import Middleware

app = FastAPI()
db = Mongo()
crypto_context = CryptoContext()
middle = Middleware(db=db, crypto_context=crypto_context)


@app.post("/user/signup", tags=["auth"])
async def create_user(user: UserRegister = Depends()) -> dict:
    result = await db.add_user(user)
    return result


@app.post("/token", response_model=Token, tags=["auth"])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> dict:
    res = await middle.login_handle(form_data.username, form_data.password)
    return res


@app.get("/run", tags=["app"])
async def get_main_data(
    current_user: User = Depends(middle.get_current_active_user),
) -> dict:
    return {"message": "Hello World"}


@app.get("/me", tags=["app"])
async def get_extracted_token(
    request: Request, current_user: User = Depends(middle.get_current_active_user)
) -> dict:
    token = request.headers["authorization"].split(" ")[1]
    payload = middle.decode_jwt_token(token)
    return {"extracted_data": payload}
