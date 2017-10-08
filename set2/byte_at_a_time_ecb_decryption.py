import sys
from Crypto.Cipher import AES
from Crypto import Random

def random_key():
    return Random.new().read(AES.block_size)

def encryption_oracle(key, msg):
    return AES.new(key, AES.MODE_ECB).encrypt(msg + ''.join(['\x04' for i in range(16 - (len(msg) % 16))]) if len(msg) % 16 != 0 else msg)

pt1 = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg\n"
pt2 = "aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq\n"
pt3 = "dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg\n"
pt4 = "YnkK"
aaa = "AAAAAAAAAAAAAAA"

plaintext = aaa + str(pt1 + pt2 + pt3 + pt4).decode("base64") # no peeking!
key = random_key()

for i in range(len(plaintext)):
    dict = {encryption_oracle(key, aaa + chr(j)) : chr(j) for j in range(0xff)}
    cipher = encryption_oracle(key, plaintext[i:])
    sys.stdout.write(dict[cipher[:AES.block_size]])
    aaa = aaa[1:]  + dict[cipher[:AES.block_size]]
