from ext import EXT_CONTEXT
from ext.utils.db_utils import object_to_dict
from model2.role.model import Role


class RoleDao(object):
    def add(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        if not params and params.keys().__contains__('name'):
            raise Exception("add role, params[name] is not existed")

        with EXT_CONTEXT["db"].session_maker() as session:
            new_user = Role(name=params.get("name"))
            session.add(new_user)
            return object_to_dict(new_user)

    def find(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))
        if not params and params.keys().__contains__('id'):
            raise Exception("find user, params[id] is not existed")

        with EXT_CONTEXT["db"].session_maker() as session:
            role = session.query(Role).filter(Role.id == params.get("id")).one()
            if role:
                print('type:', type(role))
                print('name:', role.name)
                return object_to_dict(role)
            else:
                return None

    def page(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        if not params and params.keys().__contains__('id'):
            raise Exception("find user, params[id] is not existed")

        with EXT_CONTEXT["db"].session_maker() as session:
            list = session.query(Role).filter(Role.id == params.get("id")).all()
            if list:
                print('type:', type(list))
                return object_to_dict(list)
            else:
                return None
