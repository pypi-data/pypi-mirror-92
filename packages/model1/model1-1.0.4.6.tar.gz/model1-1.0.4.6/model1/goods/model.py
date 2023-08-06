from skyext.base_class.model_base import BaseModel
from sqlalchemy import Column, Integer, String


class Goods(BaseModel):

    __tablename__ = 'goods'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))

    def __init__(self, name):
        self.name = name