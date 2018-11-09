from fastText import FastText

classifier = FastText.load_model('slack_model.bin')

text = input('Please enter a notification-text: ')

output = classifier.predict([text])[0][0][0]

channelToWorkMap = {
    '__label__-00_announcements': True,
    '__label__-01_general': True,
    '__label__-07_community': False,
    '__label__-12_random-fun': False,
    '__label__unrestricted-chat': False
}

if channelToWorkMap[output]:
    print('New message in ' + output)
else:
    print('(silence)')
