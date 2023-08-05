from model2.common_utils import resp_result
from model2.role.dao import RoleDao


class Service(object):

    def _api_get(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        user = RoleDao()
        return resp_result(data=user.find(**params))

    def _api_get_page(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        user = RoleDao()
        return resp_result(data=user.find(**params))


    def _api_post(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        user = RoleDao()
        ret_user = user.add(**params)
        return resp_result(data=ret_user)


if __name__ == '__main__':
    ser = Service()
    # print(ser._api_get(id=2))
    # print(ser._api_get_page(id=2))
    print(ser._api_post(name="abc22"))
