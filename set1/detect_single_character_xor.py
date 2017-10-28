with open('files/4.txt') as f:
    hex_strings = f.read().splitlines()

for hex in hex_strings:
    for plaintext in [''.join([chr(x ^ ord(a)) for a in hex.decode("hex")]) for x in range(128)]:
        if " the " in plaintext:
            print plaintext
