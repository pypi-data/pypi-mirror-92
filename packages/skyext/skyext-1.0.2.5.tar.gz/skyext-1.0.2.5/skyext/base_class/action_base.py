import inspect
from skyext.decorator.validator import validator_decorator


class BaseAction(object):
    _decorators = [validator_decorator]
    _is_validator_decorator = True

    def __new__(cls, *args, **kwargs):
        if cls._is_validator_decorator:
            if cls._decorators:
                for _decorator in cls._decorators:
                    for name, value in inspect.getmembers(cls):
                        if name.startswith("__") or name.startswith("_"):
                            continue

                        ded_fun = _decorator(getattr(cls, name))
                        setattr(cls, name, ded_fun)

        return object.__new__(cls)

    def _get_app_validator_forms(self, cls_name=None, _fun_name=None, **kwargs):
        pass
