from Crypto.Cipher import AES
from Crypto import Random

pt1 = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg\n"
pt2 = "aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq\n"
pt3 = "dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg\n"
pt4 = "YnkK"

key = Random.new().read(AES.block_size)
plaintext = str(pt1 + pt2 + pt3 + pt4).decode("base64") # no peeking!

def encryption_oracle(msg):
    pad_len = AES.block_size - (len(msg + plaintext) % AES.block_size)
    return AES.new(key, AES.MODE_ECB).encrypt(msg + plaintext + ''.join([chr(pad_len) for i in range(pad_len)]))

def find_len_of_padding():
    for i in range(AES.block_size):
        if len(encryption_oracle(''.join('\x00' for j in range(i)))) != len(encryption_oracle(''.join('\x00' for j in range(i + 1)))):
            return i + 1

aaa = buf = "AAAAAAAAAAAAAAA"

for i in range(len(encryption_oracle('')) - find_len_of_padding()):
    dict = {encryption_oracle(aaa[i:] + chr(j))[:AES.block_size] : chr(j) for j in range(0xff)}
    cipher = encryption_oracle(buf[i % AES.block_size:])
    aaa += dict[cipher[AES.block_size * (i / AES.block_size) : AES.block_size * ((i + AES.block_size) / AES.block_size)]]

print aaa[AES.block_size - 1:]
