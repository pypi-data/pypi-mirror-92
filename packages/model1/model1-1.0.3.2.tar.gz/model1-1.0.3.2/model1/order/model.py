from skyext import EXT_CONTEXT
from sqlalchemy import Column, Integer, String


class Order(EXT_CONTEXT["db"].Model):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))

    def __init__(self, name):
        self.name = name
