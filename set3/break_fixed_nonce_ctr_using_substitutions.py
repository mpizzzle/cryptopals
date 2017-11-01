from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util import Counter

key = Random.new().read(AES.block_size)

with open('files/19.txt') as f:
    ciphertexts = [AES.new(key, AES.MODE_CTR, counter=Counter.new(64,initial_value=0,little_endian=True,prefix="\x00\x00\x00\x00\x00\x00\x00\x00")).encrypt(line) for line in f.read().splitlines()]

for ct in ciphertexts:
    print ct
