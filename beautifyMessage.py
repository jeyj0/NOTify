import re


def beautifyMessage(text):
    text = text.strip()
    text = re.sub('\n', ' ', text)
    text = re.sub(' +', ' ', text)
    text = text.lower()
    text = re.sub(r'<@.*>', 'MENTION', text)
    text = re.sub(r'[^0-9A-Za-z\s]', '', text)
    return text
