import json


def resp_result(status=200, data=None, message=""):
    result = {
        "status": status,
        "data": data,
        "message": message
    }
    return json.dumps(result)
