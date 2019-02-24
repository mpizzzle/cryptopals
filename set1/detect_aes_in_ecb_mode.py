from sets import Set

file = open('files/8.txt').read().splitlines()

for ciphertext in file:
    charlist = [0 for x in range(256)]

    for char in ciphertext.decode("hex"):
        charlist[ord(char)] += 1

    for char in charlist:
        if char > 5:
            print ciphertext
            break

for ciphertext in file:
    split_cipher = [ciphertext[i:i + 32] for i in range(0, len(ciphertext), 32)]
    if len(split_cipher) != len(Set(split_cipher)):
        print ciphertext
