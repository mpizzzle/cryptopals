from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util import Counter

key = Random.new().read(AES.block_size)

def encrypt(plaintext):
    return AES.new(key, AES.MODE_CTR, counter=Counter.new(128)).encrypt(plaintext)

def xor(a, b):
    return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b)])

def edit(ciphertext, offset, newtext):
    plaintext = encrypt(ciphertext)
    return encrypt(plaintext[:offset] + newtext + plaintext[offset + len(newtext):])

ciphertext = encrypt(open('files/25.txt').read())
injected = ''.join(['A' for i in range(len(ciphertext))])
modified_ciphertext = edit(ciphertext, 0, injected) 

deciphered_plaintext = xor(injected, xor(ciphertext, modified_ciphertext))
print deciphered_plaintext
