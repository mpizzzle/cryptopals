from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Random import random

key = Random.new().read(AES.block_size)
iv  = Random.new().read(AES.block_size)

with open('files/17.txt') as f:
    split_file = f.read().splitlines()

def encryption_oracle():
    plaintext = split_file[random.randint(0, 9)]
    pad_len = AES.block_size - (len(plaintext) % AES.block_size)
    return AES.new(key, AES.MODE_CBC, iv).encrypt(plaintext + ''.join([chr(pad_len) for i in range(pad_len)]))

def decrypt_and_validate_padding(ciphertext):
    return pkcs7_padding_validator(AES.new(key, AES.MODE_CBC, iv).decrypt(ciphertext))

def pkcs7_padding_validator(msg):
    if ord(msg[len(msg) - 1]) > AES.block_size or ord(msg[len(msg) - 1]) == 0:
        return False
    for c in msg[:len(msg) - ord(msg[len(msg) - 1]) - 1 : -1]:
        if c != msg[len(msg) - 1]:
            return False
    return True

def pkcs7_padding_stripper(msg):
    if ord(msg[len(msg) - 1]) > AES.block_size or ord(msg[len(msg) - 1]) == 0:
        raise Exception("invalid pkcs7 padding")
    for c in msg[:len(msg) - ord(msg[len(msg) - 1]) - 1 : -1]:
        if c != msg[len(msg) - 1]:
            raise Exception("invalid pkcs7 padding")
    return msg[:len(msg) - ord(msg[len(msg) - 1])]

ciphertext = iv + encryption_oracle()
plaintext = ""

for b_idx in reversed(range((len(ciphertext) / AES.block_size) - 1)):
    blocks = [ciphertext[i : i + AES.block_size] for i in range(0, len(ciphertext), AES.block_size)]
    block = list(blocks[b_idx])
    padding = []

    for i in range(AES.block_size):
        byte = block[AES.block_size - i - 1]
        found = False

        for j in range(0xff):
            if chr(j) != byte:
                block[AES.block_size - i - 1] = chr(j)
                blocks[b_idx] = ''.join(block)

                if decrypt_and_validate_padding(''.join(blocks[:b_idx + 2])):
                    plaintext += chr(j ^ ord(byte) ^ (i + 1))
                    padding.append(j)

                    for k in range(i + 1):
                        block[AES.block_size - k - 1] = chr(padding[k] ^ (k + 1) ^ (i + 2))

                    found = True
                    break

        if not found:
            plaintext += chr(i + 1)
            padding.append(ord(byte))

            for k in range(i + 1):
                block[AES.block_size - k - 1] = chr(padding[k] ^ (k + 1) ^ (i + 2))

print pkcs7_padding_stripper(plaintext[::-1]).decode("base64")
