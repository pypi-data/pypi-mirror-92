from ext.utils.resp_utils import resp_result

from model1.goods.dao import GoodsDao


class Service(object):

    def _api_get(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        user = GoodsDao()
        return resp_result(data=user.find(**params))

    def _api_get_page(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        user = GoodsDao()
        return resp_result(data=user.page(**params))


    def _api_post(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        user = GoodsDao()
        ret_user = user.add(**params)
        return resp_result(data=ret_user)


if __name__ == '__main__':
    ser = Service()
    # print(ser._api_get(id=2))
    # print(ser._api_get_page(id=2))
    print(ser._api_post(name="abc22"))
