from model1.base_action import Model1BaseAction
from model1.goods.main import GoodsManager


class GoodsAction(Model1BaseAction):
    def get(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        main = GoodsManager()
        return main.get(**params)

    def post(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        main = GoodsManager()
        return main.post(**params)


    def delete(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        main = GoodsManager()
        return main.delete(**params)


    def put(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        main = GoodsManager()
        return main.put(**params)
