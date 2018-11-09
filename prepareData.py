import re
from os import listdir
from random import shuffle
from math import ceil

from loadFromJSONString import loadFromJSONString
from beautifyMessage import beautifyMessage

datapath = "./data"
messages = []
link_pattern = re.compile("^<https?://.*")


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


def makeAllChannelsHaveEqualMessages(messages):
    channels = {}
    for msg in messages:
        channel = msg[0]
        if channel in channels:
            channels[channel] = channels[channel] + 1
        else:
            channels[channel] = 1

    minimumMessageCountPerChannel = 999999999999

    for ch in channels:
        if channels[ch] < minimumMessageCountPerChannel:
            minimumMessageCountPerChannel = channels[ch]

    filteredMessages = []
    filteredMessageCounts = {}

    for msg in messages:
        channelName = msg[0]
        if not channelName in filteredMessageCounts:
            filteredMessageCounts[channelName] = 1
        else:
            filteredMessageCounts[channelName] = filteredMessageCounts[channelName] + 1

        if not filteredMessageCounts[channelName] > minimumMessageCountPerChannel:
            filteredMessages.append(msg)

    print("min: " + str(minimumMessageCountPerChannel))
    print("filteredMsgs: " + str(len(filteredMessages)))

    return filteredMessages


def notIn(originalMessages, messages):
    msgs = []
    for msg in originalMessages:
        if not msg in messages:
            msgs.append(msg)
    return msgs


o_msgs = messages
messages = makeAllChannelsHaveEqualMessages(messages)

messagesNotInFilteredMessages = notIn(o_msgs, messages)

shuffle(messages)
separated_messages = separateMessages(messages)

for msg in messagesNotInFilteredMessages:
    separated_messages[1].append(msg)

print("add. Msgs for validation: " + str(len(messagesNotInFilteredMessages)))

writeMessagesToFileInCorrectFormat(
    separated_messages[0], './training_data.txt')
writeMessagesToFileInCorrectFormat(
    separated_messages[1], './validation_data.txt')
