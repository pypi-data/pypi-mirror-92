from skyext import create_ext, EXT_CONTEXT

from model1.goods.main import GoodsManager


def init_test_db():
    config = Config
    create_ext(config)


class Config(object):
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:root@127.0.0.1:5432/postgres"


# if __name__ == '__main__':
#     init_test_db()
#     print(">>>>>>>", type(EXT_CONTEXT.get("db")))
#
#     main = GoodsManager()
#     main.get_test(id=1)


