from db import db

from model2.common_utils import object_to_dict
from model2.user.model import User


class UserDao(object):

    def add(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        if not params and params.keys().__contains__('id'):
            raise Exception("find user, params[id] is not existed")

        with db.session_maker() as session:
            new_user = User(name='userNNNNNNN666')
            session.add(new_user)

    def find(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        if not params and params.keys().__contains__('id'):
            raise Exception("find user, params[id] is not existed")

        with db.session_maker() as session:
            user = session.query(User).filter(User.id == params.get("id")).one()
            if user:
                print('type:', type(user))
                print('name:', user.name)
                return object_to_dict(user)
            else:
                return None


    def page(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        if not params and params.keys().__contains__('id'):
            raise Exception("find user, params[id] is not existed")

        with db.session_maker() as session:
            user = session.query(User).filter(User.id == params.get("id")).one()
            if user:
                print('type:', type(user))
                print('name:', user.name)
                return object_to_dict(user)
            else:
                return None
