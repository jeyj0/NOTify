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


def logNotification(msg):
    print(msg)
    with open('NOTify.log', 'a') as log:
        log.write(msg + '\n')


def handleNotification(text):
    output = classifier.predict([text])[0][0][0]

    # re-weight all outputs based on

    if channelToWorkMap[output]:
        logNotification('New message in ' + output)
    else:
        logNotification('(silence)')


@app.route('/notify', methods=['POST'])
def notify():
    data = request.data
    text = loadFromJSONString(str(data)[2:-1]).text
    # text = re.sub('\\\\', '\\', text)
    text = beautifyMessage(text)
    handleNotification(text)
    return request.data


@app.route('/', methods=['GET'])
def index():
    with open('index.html', 'r') as index:
        return index.read()


if __name__ == '__main__':
    app.run()
