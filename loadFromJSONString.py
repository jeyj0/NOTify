import json
from collections import namedtuple


def loadFromJSONString(data):
    return json.loads(data, object_hook=lambda d: namedtuple(
        'X', d.keys())(*d.values()))
