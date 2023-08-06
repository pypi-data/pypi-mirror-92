import os


def encrypt(filename):
    fte = open(filename, "rb").read()
    size = len(fte)
    key = os.urandom(size)
    with open(filename + ".key", "wb") as ko:
        ko.write(key)
    encrypted = bytes(a ^ b for (a, b) in zip(fte, key))
    with open(filename, "wb") as eo:
        eo.write(encrypted)


def decrypt(filename, key):
    file = open(filename, "rb").read()
    key = open(key, "rb").read()
    decrypted = bytes(a ^ b for (a, b) in zip(file, key))
    with open("decrypted." + filename, "wb") as do:
        do.write(decrypted)
