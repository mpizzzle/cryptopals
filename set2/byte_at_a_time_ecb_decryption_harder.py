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
rand_buffer = Random.new().read(random.randint(0, 100))

def encryption_oracle(msg):
    padding = ''

    if len(rand_buffer + msg + plaintext) % AES.block_size != 0:
        padding = ''.join(['\x04' for i in range(AES.block_size - (len(rand_buffer + msg + plaintext) % AES.block_size))])

    return AES.new(key, AES.MODE_ECB).encrypt(rand_buffer + msg + plaintext + padding)

def find_len_of_random_prefix():
    prefix_len = -1
    a_blocks = b_blocks = []

    for i in range(AES.block_size):
        estimate = 0
        cipher_a = encryption_oracle(''.join('\x00' for j in range(i)))
        cipher_b = encryption_oracle(''.join("\x00" for j in range(i + 1)))
        a_blocks = [cipher_a[j:j + AES.block_size] for j in range(0, len(cipher_a), AES.block_size)]
        b_blocks = [cipher_b[j:j + AES.block_size] for j in range(0, len(cipher_b), AES.block_size)]

        for a, b in zip(a_blocks, b_blocks):
            if a == b:
                estimate += AES.block_size
            else:
                if prefix_len == -1:
                    prefix_len = estimate
                if prefix_len != estimate:
                    return prefix_len + AES.block_size - i
                break

    return sum([AES.block_size if a == b else 0 for a, b in zip(a_blocks, b_blocks)])

prefix = find_len_of_random_prefix()
mod = AES.block_size - prefix % AES.block_size
buf = aaa = "AAAAAAAAAAAAAAA"
aa = ''.join("A" for i in range(mod))

for i in range(len(encryption_oracle('')) - prefix):
    dict = {encryption_oracle(aa + aaa[i:] + chr(j))[mod + prefix : mod + prefix + AES.block_size] : chr(j) for j in range(0xff)}
    cipher = encryption_oracle(aa + buf[i % AES.block_size:])
    aaa += dict[cipher[mod + prefix + (AES.block_size * (i / AES.block_size)) : mod + prefix + (AES.block_size * ((i + AES.block_size) / AES.block_size))]]

print aaa[AES.block_size - 1:]
