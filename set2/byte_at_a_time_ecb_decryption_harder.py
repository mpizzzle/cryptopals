import sys
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Random import random

pt1 = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg\n"
pt2 = "aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq\n"
pt3 = "dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg\n"
pt4 = "YnkK"

key = Random.new().read(AES.block_size)
plaintext = str(pt1 + pt2 + pt3 + pt4).decode("base64") # no peeking!
randbuffer = Random.new().read(55)

def encryption_oracle(msg):
    return AES.new(key, AES.MODE_ECB).encrypt(randbuffer + msg + plaintext + ''.join(['\x04' for i in range(AES.block_size - (len(randbuffer + msg + plaintext) % AES.block_size))]) if len(randbuffer + msg + plaintext) % AES.block_size != 0 else randbuffer + msg + plaintext)

def find_len_of_random_prefix():
    prefix_len = 0
    a = encryption_oracle('')
    b = encryption_oracle('a')

    a_blocks = [a[i:i + AES.block_size] for i in range(0, len(a), AES.block_size)]
    b_blocks = [b[i:i + AES.block_size] for i in range(0, len(b), AES.block_size)]

    for block_a, block_b in zip(a_blocks, b_blocks):
        if block_a == block_b:
            prefix_len += AES.block_size

    return prefix_len


prefix_len = 55#find_len_of_random_prefix()
mod = AES.block_size - prefix_len % AES.block_size
aaa = "AAAAAAAAAAAAAAA"
buf = aaa + ''.join("A" for i in range(mod))

for i in range(len(encryption_oracle('')) - prefix_len):
    dict = {encryption_oracle(''.join("A" for i in range(mod)) + aaa[i:] + chr(j))[prefix_len + mod : prefix_len + mod + AES.block_size] : chr(j) for j in range(0xff)}
    cipher = encryption_oracle(buf[i % AES.block_size:])
    aaa += dict[cipher[prefix_len + mod + (AES.block_size * (i / AES.block_size)) : prefix_len + mod + (AES.block_size * ((i + AES.block_size) / AES.block_size))]]
print aaa[AES.block_size - 1:]
