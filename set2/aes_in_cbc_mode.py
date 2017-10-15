from Crypto.Cipher import AES

with open('files/10.txt') as f:
    file = f.read().decode("base64")

split_file = [file[i:i + AES.block_size] for i in range(0, len(file), AES.block_size)]
key = "YELLOW SUBMARINE"
aes = AES.new(key, AES.MODE_ECB)
iv = ''.join(['\x00' for i in range(AES.block_size)])
plaintext = ""

for cipher_text in split_file:
    plaintext += ''.join([chr(ord(a) ^ ord(b)) for a, b in zip(iv, aes.decrypt(cipher_text))])
    iv = cipher_text

print plaintext
