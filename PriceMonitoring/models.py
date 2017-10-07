from peewee import *

database = MySQLDatabase('price_monitor', **{'host': '127.0.0.1', 'password': 'root', 'user': 'root'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Items(BaseModel):
    name = TextField()
    price_xpath = TextField()
    url = TextField()

    class Meta:
        db_table = 'items'

class Prices(BaseModel):
    created_at = DateTimeField()
    item = ForeignKeyField(db_column='item_id', rel_model=Items, to_field='id')
    price = IntegerField()
    price_original = TextField()

    class Meta:
        db_table = 'prices'

