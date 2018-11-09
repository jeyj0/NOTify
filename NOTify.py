from fastText import FastText

classifier = FastText.load_model('slack_model.bin')

text = input('Please enter a notification-text: ')

output = classifier.predict([text])[0][0][0]
print('I would say this notification comes from the channel: ' + output)
