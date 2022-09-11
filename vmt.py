# Virtual Money Transaction - Debug tool
# Written by Naxii
# (c) Naxii.

import sys
from peewee import *
from models import *
from uuid import uuid4

db = SqliteDatabase("db.sqlite3")

def info(text):
    print(f"[INFO] => {text}")

def debugger():
    opt = sys.argv
    if opt[1] == "select":
        if opt[2] is None:
            raise Exception("N/A")
        else:
            info(dbg_db_select(opt[2]))
    elif opt[1] == "shopgen":
        name = opt[2]
        id = str(uuid4())[:5]
        Shop.create(name=name, shopid=id)
        info(f"SUCCESS.")
        info(f"ID: {id}")
            
    else:
        raise Exception("No such option.")

def dbg_db_select(table: str):
    try:
        with db.atomic():
            if table == "User":
                query = User.select()
            elif table == "Shop":
                query = Shop.select()
            elif table == "SettlementLog":
                query = SettlementLog.select()
    except Exception as e:
        db.rollback()
        raise Exception("No such table")
    
    return query
    


if __name__ == "__main__":
    debugger()