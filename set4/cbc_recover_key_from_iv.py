import re
from Crypto.Cipher import AES
from Crypto import Random

key = Random.new().read(AES.block_size)

def encrypt(msg):
    pad_len = AES.block_size - (len(msg) % AES.block_size)
    return AES.new(key, AES.MODE_CBC, key).encrypt(msg + ''.join([chr(pad_len) for x in range(pad_len)]))

def decrypt(cipher):
    plaintext = AES.new(key, AES.MODE_CBC, key).decrypt(cipher)
    
    for c in plaintext:
        if ord(c) >= 128:
            print "invalid character found: " + plaintext
            break

    return plaintext

def xor(a, b):
    return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b)])

def encryption_oracle(m):
    return encrypt("comment1=cooking%20MCs;userdata=" + re.sub("[;|=]", '', m) + ";comment2=%20like%20a%20pound%20of%20bacon")

plaintext = "hello-admin-truehello-admin-truehello-admin-true"
ciphertext = list(encryption_oracle(plaintext))

for i in range(AES.block_size):
    ciphertext[i + AES.block_size] = '\x00'
    ciphertext[i + AES.block_size + AES.block_size] = ciphertext[i]

corrupted = decrypt(''.join(ciphertext))
recovered_key = xor(corrupted[:AES.block_size], corrupted[2 * AES.block_size : 3 * AES.block_size])

print recovered_key == key
