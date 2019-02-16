import re
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util import Counter

key = Random.new().read(AES.block_size)

def encrypt(plaintext):
    return AES.new(key, AES.MODE_CTR, counter=Counter.new(128)).encrypt(plaintext)

def decrypt_and_parse(cipher):
    return ";admin=true;" in encrypt(cipher)

def encryption_oracle(m):
    return encrypt("comment1=cooking%20MCs;userdata=" + re.sub("[;|=]", '', m) + ";comment2=%20like%20a%20pound%20of%20bacon")

plaintext = "hello-admin-true"
ciphertext = list(encryption_oracle(plaintext))

ciphertext[(2 * AES.block_size) + 5] = chr(ord('-') ^ ord(';') ^ ord(ciphertext[(2 * AES.block_size) + 5]))
ciphertext[(2 * AES.block_size) + 11] = chr(ord('-') ^ ord('=') ^ ord(ciphertext[(2 * AES.block_size) + 11]))

print decrypt_and_parse(''.join(ciphertext))
