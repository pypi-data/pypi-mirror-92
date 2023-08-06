from model2.base_action import Model2BaseAction
from model2.user.main import UserManager


class UserAction(Model2BaseAction):
    def get(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        main = UserManager()
        return main.get(**params)

    def post(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        main = UserManager()
        return main.post(**params)


    def delete(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        main = UserManager()
        return main.delete(**params)


    def put(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        main = UserManager()
        return main.put(**params)
