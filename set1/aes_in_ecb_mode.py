from Crypto.Cipher import AES

file = open('files/7.txt').read().decode("base64")

key = "YELLOW SUBMARINE"
cipher = AES.new(key, AES.MODE_ECB)

print cipher.decrypt(file)
