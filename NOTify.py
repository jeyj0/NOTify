from fastText import FastText
from flask import Flask, request
import re

from loadFromJSONString import loadFromJSONString
from beautifyMessage import beautifyMessage

app = Flask(__name__)
classifier = FastText.load_model('slack_model.bin')
channelToWorkMap = {
    '__label__-00_announcements': True,
    '__label__-01_general': True,
    '__label__-07_community': False,
    '__label__-12_random-fun': False,
    '__label__unrestricted-chat': False
}
logFileName = 'NOTify.log'
isWorkHours = True

with open(logFileName, 'w') as logFile:
    logFile.write('')


def log(msg):
    print(msg)
    with open(logFileName, 'a') as log:
        log.write(msg + '\n')


freeTimeQueue = []


def addToFreeTimeQueue(msg):
    freeTimeQueue.append(msg)


workTimeQueue = []


def addToWorkQueue(msg):
    workTimeQueue.append(msg)


def handleNotification(text):
    output = classifier.predict([text])[0][0][0]

    # re-weight all outputs based on

    shouldBeShown = channelToWorkMap[output]

    if not isWorkHours:
        shouldBeShown = not shouldBeShown

    message = 'New message in ' + output[9:]

    if shouldBeShown:
        log(message)
    else:
        if isWorkHours:
            addToFreeTimeQueue(message)
        else:
            addToWorkQueue(message)


@app.route('/notify', methods=['POST'])
def notify():
    data = request.data
    text = data.decode('utf-8')
    # text = loadFromJSONString(str(data)[2:-1]).text
    text = beautifyMessage(text)
    handleNotification(text)
    return request.data


def workThroughQueue(queue):
    for msg in queue:
        log(msg)


@app.route('/work', methods=['POST'])
def setWork():
    global isWorkHours
    isWorkHours = True
    log("--MODE: Work hours")

    global workTimeQueue
    workThroughQueue(workTimeQueue)
    workTimeQueue = []

    return '{"isWorkHours":true}'


@app.route('/free', methods=['POST'])
def setFree():
    global isWorkHours
    isWorkHours = False
    log("--MODE: Free time")

    global freeTimeQueue
    workThroughQueue(freeTimeQueue)
    freeTimeQueue = []

    return '{"isWorkHours":false}'


@app.route('/', methods=['GET'])
def index():
    with open('index.html', 'r') as index:
        return index.read()


if __name__ == '__main__':
    app.run()
