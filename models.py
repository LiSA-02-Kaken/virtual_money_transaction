from peewee import SqliteDatabase, Model, AutoField, CharField, TextField, IntegerField
from pass_hexdigest import gen_hash

db = SqliteDatabase('db.sqlite3')


class User(Model):
    id = AutoField(primary_key=True)
    name = CharField(100)
    password = CharField(128)
    refresh_token = TextField(null=True)
    balance = IntegerField(default=0)
    class Meta:
        database = db
class Shop(Model):
    id = AutoField(primary_key=True)
    name = TextField()
    shopid = TextField()
    balance = IntegerField(default=0)
    class Meta:
        database = db


db.create_tables([User])
db.create_tables([Shop])

Shop.create(name='lisa', shopid="u7ab4")
User.create(name='naxii', password=gen_hash("aiueo"))