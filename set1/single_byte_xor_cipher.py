hex = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

for plaintext in [''.join([chr(x ^ ord(a)) for a in hex.decode("hex")]) for x in range(256)]:
    if " a " in plaintext:
        print plaintext
