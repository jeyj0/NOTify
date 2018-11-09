import re
import json
from collections import namedtuple
from os import listdir
from random import shuffle

datapath = "./data"


def loadFromJSONString(data):
    return json.loads(data, object_hook=lambda d: namedtuple(
        'X', d.keys())(*d.values()))


def getChannels(path):
    return listdir(path)


def getFiles(path):
    return listdir(path)


messages = []


link_pattern = re.compile("^<https?://.*")


def meaningfulMessage(text):
    if text == '':
        return False

    if link_pattern.match(text):
        return False

    return True


def beautifyMessage(text):
    text = text.strip()
    text = re.sub('\n', ' ', text)
    text = re.sub(' +', ' ', text)
    return text


def processFile(filepath, channel):
    with open(filepath, 'r') as myfile:
        jsonString = myfile.read().replace('\n', '')
        data = loadFromJSONString(jsonString)
        for msg in data:
            if not hasattr(msg, 'subtype'):  # and not msg.subtype in subtypes:
                if meaningfulMessage(msg.text):
                    text = beautifyMessage(msg.text)
                    messages.append((channel, text))


for c in getChannels(datapath):
    channelPath = datapath + "/" + c
    if not c == ".DS_Store":
        for f in getFiles(channelPath):
            filepath = channelPath + "/" + f
            processFile(filepath, c)


def formatForFile(messages):
    output = ""
    shuffle(messages)
    for message in messages:
        output += "__label__" + message[0] + " " + message[1] + "\n"
    return output


with open('./data.txt', 'w') as datafile:
    datafile.write(formatForFile(messages))
