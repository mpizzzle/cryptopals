import sys
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Random import random

pt1 = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg\n"
pt2 = "aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq\n"
pt3 = "dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg\n"
pt4 = "YnkK"

key = Random.new().read(AES.block_size)
pt = str(pt1 + pt2 + pt3 + pt4).decode("base64") # no peeking!
r = Random.new().read(random.randint(1, 100))
aes_bs = AES.block_size

def encryption_oracle(msg):
    return AES.new(key, AES.MODE_ECB).encrypt(r + msg + pt + ''.join(['\x04' for i in range(aes_bs - (len(r + msg + pt) % aes_bs))]) if len(r + msg + pt) % aes_bs != 0 else r + msg + pt)

def find_len_of_random_prefix():
    estimate = -1

    for i in range(aes_bs):
        prefix_len = 0
        a = encryption_oracle(''.join('\x00' for j in range(i)))
        b = encryption_oracle(''.join("\x00" for j in range(i + 1)))
        a_blocks = [a[j:j + aes_bs] for j in range(0, len(a), aes_bs)]
        b_blocks = [b[j:j + aes_bs] for j in range(0, len(b), aes_bs)]

        for block_a, block_b in zip(a_blocks, b_blocks):
            if block_a == block_b:
                prefix_len += aes_bs
            else:
                if estimate == -1:
                    estimate = prefix_len
                if estimate != prefix_len:
                    return estimate + aes_bs - i
                break
    return 0

prefix = find_len_of_random_prefix()
mod = aes_bs - prefix % aes_bs
buf = aaa = "AAAAAAAAAAAAAAA"
aa = ''.join("A" for i in range(mod))

for i in range(len(encryption_oracle('')) - prefix):
    dict = {encryption_oracle(aa + aaa[i:] + chr(j))[prefix + mod : prefix + mod + aes_bs] : chr(j) for j in range(0xff)}
    cipher = encryption_oracle(aa + buf[i % aes_bs:])
    aaa += dict[cipher[prefix + mod + (aes_bs * (i / aes_bs)) : prefix + mod + (aes_bs * ((i + aes_bs) / aes_bs))]]

print aaa[aes_bs - 1:]
