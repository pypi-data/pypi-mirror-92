from model2.role.main import RoleManager


class GoodsAction(object):
    def get(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        main = RoleManager()
        return main.get(**params)

    def post(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        main = RoleManager()
        return main.post(**params)


    def delete(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        main = RoleManager()
        return main.delete(**params)


    def put(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        main = RoleManager()
        return main.put(**params)
