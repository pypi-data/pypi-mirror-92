from model1.goods.main import GoodsManager


class GoodsAction(object):
    def get(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        main = GoodsManager()
        return main.get_test(**params)

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
