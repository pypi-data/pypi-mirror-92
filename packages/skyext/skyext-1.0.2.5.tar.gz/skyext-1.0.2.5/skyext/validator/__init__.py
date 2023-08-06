from skyext.validator.base_form import BaseForm
from skyext.validator.field import BaseField
from skyext.validator.validators import Required, Length, NumberRange


class LoginForm(BaseForm):
    name = BaseField(validators=[Required(), Length(min=5, max=10), NumberRange(min=5, max=10)])

if __name__ == '__main__':
    form = LoginForm()
    request_data = {"name": 6}
    ret, errors = form.validate(request_data)
    print("验证结果", ret, str(errors))