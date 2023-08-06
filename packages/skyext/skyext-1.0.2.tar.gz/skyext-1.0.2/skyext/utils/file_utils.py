import json
import os


class FileUtils(object):
    @staticmethod
    def get_files_in_path(file_path, file_type=None):
        files = os.listdir(file_path)
        _ret_list = []
        for file in files:
            if not os.path.isdir(file):
                if file_type and not file.endswith(file_type):
                    continue
                file_url = os.path.join(file_path, file)
                _ret_list.append(file_url)

        return _ret_list

    @staticmethod
    def get_json_from_file(file_path, encoding='utf-8'):
        if not file_path:
            return

        with open(file_path, 'r', encoding=encoding) as load_f:
            load_dict = json.load(load_f)
        return load_dict
