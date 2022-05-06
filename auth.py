from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
from models import User
from secret import JWT_TOKEN, OAUTH_TOKEN
from pass_hexdigest import gen_hash

scheme = OAuth2PasswordBearer(tokenUrl=OAUTH_TOKEN)

#認証後、userを返す
def authenticate(name: str, password: str):
    user = User.get(name=name)
    if user.password != gen_hash(password):
        raise HTTPException(status_code=401, detail="Password does not match.")
    return user

def generate_tokens(user_id: int, return_type = None):

    access_pl = {
        'token_type': 'access_token',
        'exp': datetime.utcnow() + timedelta(minutes=60),
        'user_id': user_id,
    }
    refresh_pl = {
        'token_type': 'refresh_token',
        'exp': datetime.utcnow() + timedelta(days=60),
        'user_id': user_id,
    }

    access_token = jwt.encode(access_pl, JWT_TOKEN, algorithm="HS256")
    refresh_token = jwt.encode(refresh_pl, JWT_TOKEN, algorithm="HS256")

    User.update(refresh_token=refresh_token).where(User.id == user_id).execute()

    if return_type == "access":
        return access_token
    elif return_type == "refresh":
        return refresh_token

    return {'access_token': access_token, 'refresh_token': refresh_token, 'type': 'bearer'}


def get_user_from_token(token: str, token_type: str):
    try:
        payload = jwt.decode(token, JWT_TOKEN, algorithms=['HS256'])
    except JWTError:
        raise HTTPException(status_code=419, detail="Token expired")

    if payload['token_type'] != token_type:
        raise HTTPException(status_code=401, detail='Token type does not match.')
    
    user = User.get_by_id(payload['user_id'])

    if token_type == 'refresh_token' and user.refresh_token != token:
        raise HTTPException(status_code=401, detail='Refresh token does not match.')
    

    return user


async def get_user(token: str = Depends(scheme)):
    return get_user_from_token(token, 'access_token')

async def get_user_from_refresh_token(token: str = Depends(scheme)):
    return get_user_from_token(token, 'refresh_token')

