from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Random import random
from sets import Set

def random_key():
    return Random.new().read(AES.block_size)

def encryption_oracle(key, msg):
    plaintext = msg
    ciphertext = ""

    for i in range(random.randint(5, 10)):
        plaintext = '\x04' + plaintext
    for i in range(random.randint(5, 10)):
        plaintext += '\x04'

    mod = len(plaintext) % 16

    if mod != 0:
        for i in range(16 - mod):
            plaintext = plaintext + '\x04'

    if random.randint(0, 1):
        ciphertext = AES.new(key, AES.MODE_ECB).encrypt(plaintext)
        print '1'
    else:
        ciphertext += AES.new(key, AES.MODE_CBC, random_key()).encrypt(plaintext)
        print '0'

    return ciphertext

with open('files/10_decrypted.txt') as f:
    file = f.read()

ciphertext = encryption_oracle(random_key(), file)
blocks = [ciphertext[i:i + 16] for i in range(0, len(ciphertext), 16)]

if len(blocks) != len(Set(blocks)):
    print '1'
else:
    print '0'
