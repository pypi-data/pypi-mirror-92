from skyext.validator import BaseForm
from skyext.validator import Required, Length, NumberRange
from skyext.validator.field import NumberField, StringField, FileField


def make_form(service_method, field_config):
    if not field_config:
        return

    # 组装验证参数
    _field_dict = dict()
    for _field_config in field_config:
        field_name = _field_config["name"]
        field_type = _field_config["type"]
        field_validators = _field_config["validators"]
        wtform_field = _get_wtform_field(field_type, field_validators)
        _field_dict[field_name] = wtform_field

    # 动态生成form
    list(_field_dict.keys()).sort()
    name = str('Form' + service_method + str(list(_field_dict.keys())))

    return type(name, (BaseForm,), _field_dict)


def _get_wtform_field(field_type, field_validators):
    if not field_type:
        return

    field_type = str(field_type).lower()
    switch = {
        "number": ValidatorField(field_validators).new_number_filed,
        "string": ValidatorField(field_validators).new_string_filed,
        "date": ValidatorField(field_validators).new_date_filed,
        "file": ValidatorField(field_validators).new_file_filed,
    }
    wtform_field = switch[field_type]()
    return wtform_field


class ValidatorField(object):
    def __init__(self, field_validators):
        self.field_validators = field_validators

    def new_number_filed(self):
        _validator_list = _get_validator_list(self.field_validators)
        return NumberField(validators=_validator_list)

    def new_string_filed(self):
        _validator_list = _get_validator_list(self.field_validators)
        return StringField(validators=_validator_list)

    def new_date_filed(self):
        pass
        # _validator_list = _get_validator_list(self.field_validators)
        # return DateField(validators=_validator_list)

    def new_file_filed(self):
        _validator_list = _get_validator_list(self.field_validators)
        return FileField(validators=_validator_list)


def _get_validator_list(field_validators):
    if not field_validators:
        return

    _validators = []
    for field_validator in field_validators:
        _validator_type = field_validator["type"]
        _ret_validator = _get_wtform_validator(_validator_type, field_validator)
        if _ret_validator:
            _validators.append(_ret_validator)

    return _validators


def _get_wtform_validator(validator_type, field_validator):
    if not validator_type:
        return

    validator_type = str(validator_type).lower()
    switch = {
        "required": Validator(field_validator).new_required,
        "range": Validator(field_validator).new_range,
        "length": Validator(field_validator).new_length,
        "email": Validator(field_validator).new_email,
        "regexp": Validator(field_validator).new_regexp
    }
    ret_field_validator = switch[validator_type]()
    return ret_field_validator


class Validator(object):

    def __init__(self, validator_params):
        self.validator_params = validator_params

    def new_required(self):
        msg = self.validator_params["message"]
        return Required(message=msg)

    def new_range(self):
        msg = self.validator_params["message"]
        min = self.validator_params["min"] if self.validator_params["min"] else None
        max = self.validator_params["max"] if self.validator_params["max"] else None
        return NumberRange(min=min, max=max, message=msg)

    def new_length(self):
        msg = self.validator_params["message"]
        min = self.validator_params["min"] if self.validator_params["min"] else -1
        max = self.validator_params["max"] if self.validator_params["max"] else -1
        return Length(min=min, max=max, message=msg)

    def new_email(self):
        pass

    def new_regexp(self):
        pass
