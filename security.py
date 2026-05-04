import hashlib

def HashString(msg):
    return hashlib.sha256(msg.encode()).hexdigest()



password = input("Input password: ")
hashMessage = HashString(password)
print(hashMessage)