import hashlib
import datetime


class Block():
    
    def __init__(self, user:str, target:str, balance:int, hash:str, hash_before:str, datetime:datetime.datetime):
        self.user = user
        self.target = target
        self.balance = balance
        self.hash = hash
        self.hash_before = hash_before
        self.datetime = datetime

    def view(self):
        print(
        f"""
        LAST UPDATED: {self.datetime}

        USER: {self.user}
        TARGET: {self.target}
        BALANCE: {self.balance}
        HASH: {self.hash}
        HASH_BEFORE: {self.hash_before}
        
        """)
    



