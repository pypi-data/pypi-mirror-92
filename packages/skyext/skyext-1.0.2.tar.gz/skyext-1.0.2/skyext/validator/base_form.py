from skyext.validator.field import BaseField as Field


class BaseForm(object):
    def __init__(self):
        _fields = {}
        for name, field in self.__class__.__dict__.items():
            if isinstance(field, Field):
                _fields[name] = field
        self._fields = _fields
        self.data = {}

    def validate(self, request_data):
        flag = True
        for name, field in self._fields.items():
            input_val = request_data.get(name, "")
            result = field.validate(form=self, field_name=name, field_val=input_val)
            if not result:
                flag = False

        return flag, field.errors