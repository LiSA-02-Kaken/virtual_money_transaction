from fastapi import Depends, FastAPI, Form, Request, HTTPException, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import Response
from typing import Optional
from peewee import DoesNotExist
from pydantic import BaseModel
from auth import get_user, get_user_from_refresh_token, generate_tokens, authenticate
from models import Shop, SettlementLog
import models
from secret import JWT_TOKEN
from uuid import uuid4
import datetime
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates/')

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


@app.get('/login')
async def login(request: Request):
    return templates.TemplateResponse("login.html", context={'request': request})

@app.post('/login')
async def login(request: Request, name: str = Form(...), pw: str = Form(...)):
    user = authenticate(name, pw)
    template_response =  templates.TemplateResponse("login-done.html", context={'request': request, 'name': user.name})
    template_response.set_cookie(key="access", value=str(generate_tokens(user.id, "access")))
    template_response.set_cookie(key="refresh", value=str(generate_tokens(user.id, "refresh")))
    return template_response


@app.post("/token", response_model=Token)
async def token(form: OAuth2PasswordRequestForm = Depends()):
    user = authenticate(form.username, form.password)
    return generate_tokens(user.id)

@app.get("/transaction/pay")
async def payment(request: Request):
    return templates.TemplateResponse("payment.html", context={'request': request})


@app.post("/transaction/pay")
async def payment(request: Request, user: User = Depends(get_user), pay_balance: int = Form(...), req_shop: str = Form(...)):
    try:
        shop = Shop.get(Shop.shopid == req_shop)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail='The shop does not exist.')

    if pay_balance <= 0 or pay_balance > 100000:
        raise HTTPException(status_code=400, detail="Invalid payment amount.")
    
    if user.balance < pay_balance:
        raise HTTPException(status_code=400, detail="Insufficient balance.")

    payment_balance = user.balance - pay_balance
    models.User.update(balance=payment_balance).where(models.User.id == user.id).execute()
    
    shop_balance = shop.balance
    Shop.update(balance=shop_balance+pay_balance).where(Shop.shopid == req_shop).execute()

    session_id = str(uuid4())[:8]

    SettlementLog.create(session=session_id, user=user.name, shop=shop.name, balance=pay_balance, time=datetime.datetime.now())

    return templates.TemplateResponse("done.html", context={'request': request, 'result': pay_balance, 'user': user.name, 'shop_name': shop.name, 'sid': session_id})


@app.get("/protected")
def protected(A):

    return {"result": user}


@app.get("/refresh_token", response_model=Token)
async def refresh_token(current_user: User = Depends(get_user_from_refresh_token)):
    return generate_tokens(current_user.id)

@app.get("/users/me/", response_model=User)
async def read_me(request: Request, access: Optional[str]=Cookie(None), refresh: Optional[str]=Cookie(None)):
    user = get_user_from_token(access, "access")
    # リダイレクトのホストがきもくなってる
    
    return templates.TemplateResponse("profile.html", context={'request': request, 'name': user.name, 'balance': user.balance})