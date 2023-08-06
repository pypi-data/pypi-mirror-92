from functools import wraps


def validator_decorator(func):
    @wraps(func)
    def inner(self, **kwargs):
        _class_name = self.__class__.__name__
        _fun_name = func.__name__

        _is_need_validator = hasattr(self, "_is_validator_decorator") and self._is_validator_decorator
        if _is_need_validator and self._get_app_validator_forms:
            _validator_form_dict = self._get_app_validator_forms(_class_name, _fun_name, **kwargs)
            _validate_params(_validator_form_dict, _class_name, _fun_name, **kwargs)

        return func(self, **kwargs)
    return inner


def _validate_params(validator_form_dict, cls_name, fun_name, **params):
    """
    :param validator_form_dict: 每一个业务 app 一个变量 validator_form_dict
    :param cls_name:
    :param fun_name:
    :param params:
    :return:
    """
    if not validator_form_dict:
        return

    _validator_form_key_list = [cls_name, fun_name]
    _validator_form_key = "_".join(_validator_form_key_list)
    if _validator_form_key in validator_form_dict:
        _validator_form_func = validator_form_dict[_validator_form_key]
        validate_form = _validator_form_func()
        valid_success, errors = validate_form.validate(params)
        if not valid_success:
            raise Exception("parameter error>>>>{0}".format(str(errors)))