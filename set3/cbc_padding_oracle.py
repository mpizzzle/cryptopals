from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Random import random

key = Random.new().read(AES.block_size)
iv  = Random.new().read(AES.block_size)

with open('files/17.txt') as f:
    split_file = f.read().splitlines()

def pkcs7_padding_validator(msg):
    if ord(msg[len(msg) - 1]) > AES.block_size or ord(msg[len(msg) - 1]) == 0:
        return False
    for c in msg[:len(msg) - ord(msg[len(msg) - 1]) - 1 : -1]:
        if c != msg[len(msg) - 1]:
            return False
    return True

qwer = random.randint(0, 9)
def encryption_oracle():
    plaintext = split_file[3]
    pad_len = AES.block_size - (len(plaintext) % AES.block_size)
    return AES.new(key, AES.MODE_CBC, iv).encrypt(plaintext + ''.join([chr(pad_len) for i in range(pad_len)]))

def decrypt_and_validate_padding(ciphertext):
    return pkcs7_padding_validator(AES.new(key, AES.MODE_CBC, iv).decrypt(ciphertext))

ct1 = iv + encryption_oracle()
blocks = [ct1[i:i + AES.block_size] for i in range(0, len(ct1), AES.block_size)]
pt = ""

for block in blocks[::-1][:len(blocks) - 1]:

    b = list(block)#list(blocks[len(blocks) - 2])
    blep = []

    for i in range(AES.block_size):
        ignore = b[AES.block_size - (i + 1)]
        br = False

        for j in range(0xff):
            if chr(j) != ignore:
                b[AES.block_size - (i + 1)] = chr(j)

            blocks[len(blocks) - 2] = ''.join(b)

            if decrypt_and_validate_padding(''.join(blocks)):
                pt += chr(j ^ ord(ignore) ^ (i + 1))
                print list(chr(j ^ ord(ignore) ^ (i + 1)))
                blep.append(j)

                for k in range(i + 1):
                    b[AES.block_size - (k + 1)] = chr(blep[k] ^ (k + 1) ^ (i + 2))

                br = True
                break

        if not br:
            blep.append(ord(ignore))

            for k in range(i + 1):
                b[AES.block_size - (k + 1)] = chr(blep[k] ^ (k + 1) ^ (i + 2))
            print list("br" + chr(i + 1))
            pt += chr(i + 1)

print pt[::-1]
print split_file[3]
print pt[::-1].decode("base64")
