import os

from model1 import init_app
from skyext import init_component


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI",
                                        "postgresql+psycopg2://postgres:root@127.0.0.1:5432/postgres")
    SESSION_URL = "redis://127.0.0.1:6379/0"
    CACHE_URL = "redis://127.0.0.1:6379/1"
    ELASTICSEARCH_HOST = None




if __name__ == '__main__':
    init_component(Config)
    init_app()

    # from model1.goods.action import GoodsAction
    # action2 = GoodsAction()
    # ret = action2.get(id=1)
    # print("ret >>>>>", ret)

