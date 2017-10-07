from Crypto.Cipher import AES

with open('files/7.txt') as f:
    file = f.read().decode("base64")

key = "YELLOW SUBMARINE"
cipher = AES.new(key, AES.MODE_ECB)

print cipher.decrypt(file)
