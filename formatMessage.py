from beautifyMessage import beautifyMessage

with open("message.txt", 'r') as f:
    message = beautifyMessage(f.read())
    print(message)
