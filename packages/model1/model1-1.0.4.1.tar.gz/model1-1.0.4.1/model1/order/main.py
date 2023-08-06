from skyext import EXT_CONTEXT
from skyext.utils.db_utils import query2dict
from model1.order.model import Order


class OrderManager(object):

    def get(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))
        if not params and params.keys().__contains__('id'):
            raise Exception("find user, params[id] is not existed")

        with EXT_CONTEXT["db"].session_maker() as session:
            role = session.query(Order).filter(Order.id == params.get("id")).one()
            if role:
                print('type:', type(role))
                print('name:', role.name)
                return query2dict(role)
            else:
                return None


    def post(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        if not params and params.keys().__contains__('id'):
            raise Exception("find user, params[id] is not existed")

        with EXT_CONTEXT["db"].session_maker() as session:
            list = session.query(Order).filter(Order.id == params.get("id")).all()
            if list:
                print('type:', type(list))
                return query2dict(list)
            else:
                return None

    def delete(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        if not params and params.keys().__contains__('id'):
            raise Exception("find user, params[id] is not existed")

        with EXT_CONTEXT["db"].session_maker() as session:
            _model = session.query(Order).filter(Order.id == params.get("id")).first()
            if _model:
                session.delete(_model)
                return query2dict(_model)
            else:
                return None

    def put(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        if not params and params.keys().__contains__('id'):
            raise Exception("find user, params[id] is not existed")

        if not params and params.keys().__contains__('name'):
            raise Exception("find user, params[id] is not existed")

        with EXT_CONTEXT["db"].session_maker() as session:
            _model = session.query(Order).filter(Order.id == params.get("id")).first()
            if _model:
                _model.name = params.get("name")
                return query2dict(_model)
            else:
                return None