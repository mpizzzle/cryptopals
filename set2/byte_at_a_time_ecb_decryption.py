import sys
from Crypto.Cipher import AES
from Crypto import Random

pt1 = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg\n"
pt2 = "aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq\n"
pt3 = "dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg\n"
pt4 = "YnkK"

key = Random.new().read(AES.block_size)
plaintext = str(pt1 + pt2 + pt3 + pt4).decode("base64") # no peeking!

def encryption_oracle(msg):
    return AES.new(key, AES.MODE_ECB).encrypt(msg + plaintext + ''.join(['\x04' for i in range(AES.block_size - (len(msg + plaintext) % AES.block_size))]) if len(msg + plaintext) % AES.block_size != 0 else msg + plaintext)

aaa = buf = "AAAAAAAAAAAAAAA"

for i in range(len(encryption_oracle(''))):
    dict = {encryption_oracle(aaa[i:] + chr(j))[:AES.block_size] : chr(j) for j in range(0xff)}
    cipher = encryption_oracle(buf[i % AES.block_size:])
    aaa += dict[cipher[AES.block_size * (i / AES.block_size) : AES.block_size * ((i + AES.block_size) / AES.block_size)]]

print aaa[AES.block_size - 1:]
