from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Random import random

key = Random.new().read(AES.block_size)
iv  = Random.new().read(AES.block_size)

def encryption_oracle():
    with open('files/17.txt') as f:
        plaintext = f.read().splitlines()[random.randint(0, 9)]

    pad_len = AES.block_size - (len(plaintext) % AES.block_size)
    return iv + AES.new(key, AES.MODE_CBC, iv).encrypt(plaintext + ''.join([chr(pad_len) for i in range(pad_len)]))

def pkcs7_padding_validation(msg, strip_mode):
    len_pad = ord(msg[len(msg) - 1])

    if len_pad == 0 or len_pad > AES.block_size:
        return False if not strip_mode else ""

    for c in msg[len(msg) - len_pad:]:
        if c != chr(len_pad):
            return False if not strip_mode else ""

    return True if not strip_mode else msg[:len(msg) - len_pad]

def padding_oracle(ciphertext):
    return pkcs7_padding_validation(AES.new(key, AES.MODE_CBC, iv).decrypt(ciphertext), False)

ciphertext = encryption_oracle()
plaintext = ""

for b_idx in reversed(range((len(ciphertext) / AES.block_size) - 1)):
    blocks = [ciphertext[i : i + AES.block_size] for i in range(0, len(ciphertext), AES.block_size)]
    block = list(blocks[b_idx])
    padding = []

    for i in range(AES.block_size):
        guessed_byte = block[AES.block_size - i - 1]
        found = False

        for c in range(0xff + 1):
            if chr(c) != guessed_byte:
                block[AES.block_size - i - 1] = chr(c)
                blocks[b_idx] = ''.join(block)

                if padding_oracle(''.join(blocks[:b_idx + 2])):
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

print pkcs7_padding_validation(plaintext[::-1], True).decode("base64")
