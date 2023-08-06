from functools import wraps


def validator_decorator(func):
    @wraps(func)
    def inner(self, **kwargs):
        _class_name = self.__class__.__name__
        _fun_name = func.__name__

        if self._validate:
            self._validate(_class_name, _fun_name, **kwargs)

        return func(self, **kwargs)

    return inner


def _validate_params(cls_name, fun_name, **params):
    pass
    # _validator_form_key_list = [cls_name, fun_name]
    # _validator_form_key = "_".join(_validator_form_key_list)
    # if validator_form_dict and _validator_form_key in validator_form_dict:
    #     _validator_form_func = validator_form_dict[_validator_form_key]
    #     validate_form = _validator_form_func()
    #     valid_success, errors = validate_form.validate(params)
    #     if not valid_success:
    #         raise Exception("验证异常>>>>{0}".format(str(errors)))