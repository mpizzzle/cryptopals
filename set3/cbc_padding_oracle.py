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

def pkcs7_padding_oracle(msg, strip_mode):
    if ord(msg[len(msg) - 1]) > AES.block_size or ord(msg[len(msg) - 1]) == 0:
        return False if not strip_mode else ""

    for c in msg[:len(msg) - ord(msg[len(msg) - 1]) - 1 : -1]:
        if c != msg[len(msg) - 1]:
            return False if not strip_mode else ""

    return True if not strip_mode else msg[:len(msg) - ord(msg[len(msg) - 1])]

def decrypt_and_validate_padding(ciphertext):
    return pkcs7_padding_oracle(AES.new(key, AES.MODE_CBC, iv).decrypt(ciphertext), False)

ciphertext = iv + encryption_oracle()
plaintext = ""

for b_idx in reversed(range((len(ciphertext) / AES.block_size) - 1)):
    blocks = [ciphertext[i : i + AES.block_size] for i in range(0, len(ciphertext), AES.block_size)]
    block = list(blocks[b_idx])
    padding = []

    for i in range(AES.block_size):
        guessed_byte = block[AES.block_size - i - 1]
        found = False

        for c in range(0xff):
            if chr(c) != guessed_byte:
                block[AES.block_size - i - 1] = chr(c)
                blocks[b_idx] = ''.join(block)

                if decrypt_and_validate_padding(''.join(blocks[:b_idx + 2])):
                    plaintext += chr(c ^ ord(guessed_byte) ^ (i + 1))
                    padding.append(c)

                    for p in range(i + 1):
                        block[AES.block_size - p - 1] = chr(padding[p] ^ (p + 1) ^ (i + 2))

                    found = True
                    break

        if not found:
            plaintext += chr(i + 1)
            padding.append(ord(guessed_byte))

            for p in range(i + 1):
                block[AES.block_size - p - 1] = chr(padding[p] ^ (p + 1) ^ (i + 2))

print pkcs7_padding_oracle(plaintext[::-1], True).decode("base64")
