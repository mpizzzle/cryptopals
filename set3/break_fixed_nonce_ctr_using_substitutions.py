from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util import Counter

key = Random.new().read(AES.block_size)

def encrypt(plaintext):
    return AES.new(key, AES.MODE_CTR, counter=Counter.new(128)).encrypt(plaintext)

def xor(a, b):
    return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b)])

with open('files/19.txt') as f:
    ciphertexts = [encrypt(line.decode("base64")) for line in f.read().splitlines()]

def drag_crib(crib, a_xor_b):
    derp = []
    for n in range(len(a_xor_b) - len(crib) + 1):
        potential = xor(crib, a_xor_b[n : n + len(crib)])

        #if all(x.isalpha() or x.isspace() for x in potential):
        #    if crib not in potential:
        derp.append(potential)
    print derp

for i in range(40):
    if i != 5:
        print i
        drag_crib("r polite ", xor(ciphertexts[i], ciphertexts[5]))
