from skyext.base_class.action_base import BaseAction
from model2 import validator_form_dict


class Model2BaseAction(BaseAction):
    def _get_app_validator_forms(self, cls_name, fun_name, **params):
        return validator_form_dict
