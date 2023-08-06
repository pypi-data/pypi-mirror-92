from skyext.utils.file_utils import FileUtils
from skyext.validator.parse.make_form import make_form


def get_validator_forms(config_file_path):
    _ret_config_list = load_validator_config(config_file_path)
    if not _ret_config_list:
        return

    _validator_form_dict = dict()
    for service_m in _ret_config_list:
        _service_cls = service_m["action"]
        _service_methods = service_m["methods"]

        _service_cls_name = _service_cls
        if "." in _service_cls_name:
            _service_cls_name = _service_cls_name.rsplit(".", 1)[1]

        for _service_method in _service_methods:
            _service_method_name = _service_method["name"]
            _service_method_fields = _service_method["fields"]

            # 请求参数校验
            validate_form_cls = make_form(_service_method_name, _service_method_fields)
            if validate_form_cls:
                _validator_form_key_list = [_service_cls_name, _service_method_name]
                _validator_form_key = "_".join(_validator_form_key_list)
                _validator_form_dict[_validator_form_key] = validate_form_cls

    return _validator_form_dict


def load_validator_config(config_file_path):
    file_path = config_file_path
    _json_content = FileUtils.get_json_from_file(file_path)
    if _json_content:
        return _json_content
    return []
