from hashlib import sha256
from secret import PASS_SALT
from uuid import uuid4

def gen_hash(password:str):
    before_ps = PASS_SALT + password
    hs = sha256(before_ps.encode()).hexdigest()
    return hs

def gen_uuid():
    id = str(uuid4())[:8]
    return id