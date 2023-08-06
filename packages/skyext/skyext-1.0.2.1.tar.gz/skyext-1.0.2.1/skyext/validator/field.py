import inspect
import itertools

from skyext.validator.validators import StopValidation


class BaseField(object):
    """
    Field base class
    """
    errors = tuple()
    process_errors = tuple()
    raw_data = None
    validators = tuple()

    def __init__(self, validators=None):
        self.check_validators(validators)
        self.validators = validators or self.validators

    @classmethod
    def check_validators(cls, validators):
        if validators is not None:
            for validator in validators:
                if not callable(validator):
                    raise TypeError("{} is not a valid validator because it is not "
                                    "callable".format(validator))

                if inspect.isclass(validator):
                    raise TypeError("{} is not a valid validator because it is a class, "
                                    "it should be an instance".format(validator))

    def validate(self, form=None, field_name=None, field_val=None, extra_validators=tuple()):
        self.errors = list(self.process_errors)
        stop_validation = False

        self.check_validators(extra_validators)

        if not stop_validation:
            chain = itertools.chain(self.validators, extra_validators)
            stop_validation = self._run_validation_chain(form, field_name, field_val, chain)

        return len(self.errors) == 0

    def _run_validation_chain(self, form, field_name, field_val, validators):
        for validator in validators:
            try:
                validator(form, self, field_name, field_val)
            except StopValidation as e:
                if e.args and e.args[0]:
                    self.errors.append(e.args[0])
                return True
            except ValueError as e:
                self.errors.append(e.args[0])

        return False

    def gettext(self, string):
        return string

    def ngettext(self, singular, plural, n):
        return ""


class StringField(BaseField):
    pass


class EmailField(BaseField):
    pass


class NumberField(BaseField):
    pass


class FileField(BaseField):
    pass