from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from auth import get_user, get_user_from_refresh_token, generate_tokens, authenticate
from models import Shop

app = FastAPI()

class Token(BaseModel):
    access_token: str
    refresh_token: str
    type: str
    class Config:
        orm_mode = True

class User(BaseModel):
    name: str
    balance: int
    class Config:
        orm_mode = True

@app.post("/token", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = authenticate(form.username, form.password)
    return generate_tokens(user.id)

@app.post("/transaction/pay")
async def payment(user: User = Depends(get_user)):
    user_balance = user.balance

@app.get("/refresh_token", response_model=Token)
async def refresh_token(current_user: User = Depends(get_user_from_refresh_token)):
    return generate_tokens(current_user.id)

@app.get("/users/me/", response_model=User)
async def read_me(current_user: User = Depends(get_user)):
    return current_user