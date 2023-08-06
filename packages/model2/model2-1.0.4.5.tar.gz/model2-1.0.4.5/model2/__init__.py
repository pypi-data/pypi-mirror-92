from skyext.validator.parse.validator_forms import get_validator_forms

validator_form_dict = dict()

def init_app():
    validator_file_path = 'validators.json'
    _validator_form_dict = get_validator_forms(validator_file_path)
    if _validator_form_dict:
        validator_form_dict.update(_validator_form_dict)


