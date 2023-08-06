import inspect
from skyext.decorator.validator import validator_decorator


class BaseAction(object):
    _decorators = [validator_decorator]

    def __new__(cls, *args, **kwargs):
        if cls._decorators:
            for _decorator in cls._decorators:
                for name, value in inspect.getmembers(cls):
                    if name.startswith("__") or name.startswith("_"):
                        continue

                    ded_fun = _decorator(getattr(cls, name))
                    setattr(cls, name, ded_fun)

        return object.__new__(cls)

    def _validate(self, cls_name, _fun_name, **kwargs):
        pass
