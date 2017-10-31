from Crypto.Cipher import AES

ciphertext = "L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==".decode("base64")
key = "YELLOW SUBMARINE"
nonce = ''.join(['\x00' for i in range(AES.block_size / 2)])

def encrypt(ciphertext, key, nonce):
    aes = AES.new(key, AES.MODE_ECB)
    block_count = ['\x00' for i in range(AES.block_size / 2)]
    plaintext = ""

    for block in [ciphertext[i:i + AES.block_size] for i in range(0, len(ciphertext), AES.block_size)]:
        plaintext += ''.join([chr(ord(a) ^ ord(b)) for a, b in zip(block, aes.encrypt(nonce + ''.join(block_count)))])
        block_count[0] = chr((ord(block_count[0]) + 1) % 256) #you get the point

    return plaintext

print encrypt(encrypt(encrypt(ciphertext, key, nonce), key, nonce), key, nonce)
