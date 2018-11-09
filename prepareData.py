import re
import json
from collections import namedtuple
from os import listdir
from random import shuffle
from math import ceil

from beautifyMessage import beautifyMessage

datapath = "./data"
messages = []
link_pattern = re.compile("^<https?://.*")


def loadFromJSONString(data):
    return json.loads(data, object_hook=lambda d: namedtuple(
        'X', d.keys())(*d.values()))


def getChannels(path):
    return listdir(path)


def getFiles(path):
    return listdir(path)


def meaningfulMessage(text):
    if text == '':
        return False

    if link_pattern.match(text):
        return False

    return True


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
    for message in messages:
        output += "__label__" + message[0] + " " + message[1] + "\n"
    return output


def separateMessages(messages):
    length = len(messages)
    training_percent = 4/5
    training_amount = ceil(length * training_percent)
    return (messages[:training_amount], messages[training_amount:])


def writeMessagesToFileInCorrectFormat(messages, filename):
    with open(filename, 'w') as datafile:
        datafile.write(formatForFile(messages))


shuffle(messages)
separated_messages = separateMessages(messages)

writeMessagesToFileInCorrectFormat(
    separated_messages[0], './training_data.txt')
writeMessagesToFileInCorrectFormat(
    separated_messages[1], './validation_data.txt')
