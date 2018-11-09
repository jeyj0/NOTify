import re


def beautifyMessage(text):
    text = text.strip()
    text = re.sub('\n', ' ', text)
    text = re.sub(' +', ' ', text)
    text = text.lower()
    # replace mentions with arbitrary placeholder
    return text
