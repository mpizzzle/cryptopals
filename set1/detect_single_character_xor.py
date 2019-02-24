hex_strings = open('files/4.txt') .read().splitlines()

for hex in hex_strings:
    for plaintext in [''.join([chr(x ^ ord(a)) for a in hex.decode("hex")]) for x in range(256)]:
        if " the " in plaintext:
            print plaintext
