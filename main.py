import json
from collections import namedtuple

filepath = "./data/-00_announcements/2018-10-15.json"


def loadFromJSONString(data):
    return json.loads(data, object_hook=lambda d: namedtuple(
        'X', d.keys())(*d.values()))


with open(filepath, 'r') as myfile:
    jsonString = myfile.read().replace('\n', '')
    data = loadFromJSONString(jsonString)
    print(data)
