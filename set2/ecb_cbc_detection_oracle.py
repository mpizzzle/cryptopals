from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Random import random
from sets import Set

def random_key():
    return Random.new().read(AES.block_size)

def encryption_oracle(msg):
    plaintext = msg
    ciphertext = ""

    for i in range(random.randint(5, 10)):
        plaintext = '\x00' + plaintext
    for i in range(random.randint(5, 10)):
        plaintext += '\x00'

    pad_len = AES.block_size - (len(plaintext) % AES.block_size)
    plaintext += ''.join([chr(pad_len) for i in range(pad_len)])

    if random.randint(0, 1):
        ciphertext = AES.new(random_key(), AES.MODE_ECB).encrypt(plaintext)
        print True
    else:
        ciphertext = AES.new(random_key(), AES.MODE_CBC, random_key()).encrypt(plaintext)
        print False

    return ciphertext

with open('files/10_decrypted.txt') as f:
    ciphertext = encryption_oracle(f.read())

blocks = [ciphertext[i:i + AES.block_size] for i in range(0, len(ciphertext), AES.block_size)]

print len(blocks) != len(Set(blocks))
