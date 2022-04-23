from peewee import SqliteDatabase, Model, AutoField, CharField, TextField
from pass_hexdigest import gen_hash

db = SqliteDatabase('db.sqlite3')

class User(Model):
    id = AutoField(primary_key=True)
    name = CharField(100)
    password = CharField(128)
    refresh_token = TextField(null=True)

    class Meta:
        database = db
    
db.create_tables([User])

User.create(name='naxii', password=gen_hash("aiueo"))