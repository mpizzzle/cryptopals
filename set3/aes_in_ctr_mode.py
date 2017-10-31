from Crypto.Cipher import AES

ciphertext = "L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==".decode("base64")
blocks = [ciphertext[i:i + AES.block_size] for i in range(0, len(ciphertext), AES.block_size)]

key = "YELLOW SUBMARINE"
aes = AES.new(key, AES.MODE_ECB)

nonce = ''.join(['\x00' for i in range(AES.block_size / 2)])
block_count = ['\x00' for i in range(AES.block_size / 2)]

plaintext = ""

for block in blocks:
    plaintext += ''.join([chr(ord(a) ^ ord(b)) for a, b in zip(block, aes.encrypt(nonce + ''.join(block_count)))])
    block_count[0] = chr((ord(block_count[0]) + 1) % 256) #you get the point

print plaintext
