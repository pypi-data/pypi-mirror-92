from db import db
from sqlalchemy import Column, Integer, String

class Order(db.Model):

    __tablename__ = 'order'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))

    def __init__(self, name):
        self.name = name