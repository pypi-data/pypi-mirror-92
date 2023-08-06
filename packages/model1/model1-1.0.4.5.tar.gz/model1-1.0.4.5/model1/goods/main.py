from skyext import db
from skyext.base_class.main_base import BaseMain
from skyext.utils.db_utils import query2dict
from model1.goods.model import Goods


class GoodsManager(BaseMain):

    def get(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        if not params and params.keys().__contains__('id'):
            raise Exception("find user, params[id] is not existed")

        role = db.session.query(Goods).filter(Goods.id == params.get("id")).one()
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

        if params and not params.keys().__contains__('name'):
            raise Exception("find user, params[name] is not existed")

        role = Goods(params.get("name"))
        db.session.add(role)
        db.session.commit()
        if role:
            print('type:', type(role))
            return query2dict(role)
        else:
            return None

    def delete(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        if not params and params.keys().__contains__('id'):
            raise Exception("find user, params[id] is not existed")

        _model = db.session.query(Goods).filter(Goods.id == params.get("id")).first()
        if _model:
            db.session.delete(_model)
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

        _model = db.session.query(Goods).filter(Goods.id == params.get("id")).first()
        if _model:
            _model.name = params.get("name")
            db.session.commit()
            return query2dict(_model)
        else:
            return None