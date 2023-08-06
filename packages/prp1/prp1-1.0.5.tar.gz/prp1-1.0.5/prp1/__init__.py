import json


def read_json(file_path, default=None):
    try:
        with open(file_path, encoding="utf-8") as f:
            return json.load(f)
    except:
        if default is None:
            return {}

        return default