from Crypto.Cipher import AES

with open('files/10.txt') as f:
    file = f.read().decode("base64")

split_file = [file[i:i + 16] for i in range(0, len(file), 16)]
key = "YELLOW SUBMARINE"
aes = AES.new(key, AES.MODE_ECB)
iv = "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
plaintext = ""

for cipher_text in split_file:
    plaintext += ''.join([chr(ord(a) ^ ord(b)) for a, b in zip(iv, aes.decrypt(cipher_text))])
    iv = cipher_text

print plaintext
