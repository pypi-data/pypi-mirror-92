from skyext import EXT_CONTEXT
from skyext.utils.db_utils import object_to_dict, query2dict

from model1.goods.model import Goods


class GoodsDao(object):
    def add(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        if not params and params.keys().__contains__('name'):
            raise Exception("add role, params[name] is not existed")

        with EXT_CONTEXT["db"].session_maker() as session:
            new_user = Goods(name=params.get("name"))
            session.add(new_user)
            return query2dict(new_user)


    def find(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))
        if not params and params.keys().__contains__('id'):
            raise Exception("find user, params[id] is not existed")

        with EXT_CONTEXT["db"].session_maker() as session:
            role = session.query(Goods).filter(Goods.id == params.get("id")).one()
            if role:
                print('type:', type(role))
                print('name:', role.name)
                return query2dict(role)
            else:
                return None


    def page(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        if not params and params.keys().__contains__('id'):
            raise Exception("find user, params[id] is not existed")

        with EXT_CONTEXT["db"].session_maker() as session:
            list = session.query(Goods).filter(Goods.id == params.get("id")).all()
            if list:
                print('type:', type(list))
                return query2dict(list)
            else:
                return None