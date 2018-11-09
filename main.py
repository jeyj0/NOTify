import json
from collections import namedtuple
from os import listdir

filepath = "./data/-00_announcements/2018-10-15.json"
datapath = "./data"


def loadFromJSONString(data):
    return json.loads(data, object_hook=lambda d: namedtuple(
        'X', d.keys())(*d.values()))


def getChannels(path):
    return listdir(path)


def getFiles(path):
    return listdir(path)


messages = []


def meaningfulMessage(text):
    return text != ''


def processFile(filepath, channel):
    with open(filepath, 'r') as myfile:
        jsonString = myfile.read().replace('\n', '')
        data = loadFromJSONString(jsonString)
        for msg in data:
            if not hasattr(msg, 'subtype'):  # and not msg.subtype in subtypes:
                if meaningfulMessage(msg.text):
                    messages.append((channel, msg.text))


for c in getChannels(datapath):
    channelPath = datapath + "/" + c
    for f in getFiles(channelPath):
        filepath = channelPath + "/" + f
        processFile(filepath, c)

print(messages)
