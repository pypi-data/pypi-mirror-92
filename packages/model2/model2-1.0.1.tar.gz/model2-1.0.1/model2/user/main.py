
from model2.common_utils import resp_result
from model2.user.dao import UserDao


class Service(object):

    def _api_get(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        user = UserDao()
        return resp_result(data=user.find())

    def _api_get_page(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        user = UserDao()
        return resp_result(data=user.find(**params))

    def _api_post(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        user = UserDao()
        user.add()
        return resp_result()