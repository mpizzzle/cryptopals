from Crypto.Cipher import AES

with open('files/8.txt') as f:
    file = f.read().splitlines()

for ciphertext in file:
    charlist = [0 for x in range(256)]

    for char in ciphertext.decode("hex"):
        charlist[ord(char)] += 1

    for char in charlist:
        if char > 5:
            print ciphertext.decode("hex")
            print charlist
            break
