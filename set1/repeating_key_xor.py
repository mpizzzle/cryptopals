def encrypt(key, msg):
    return ''.join([chr(ord(key[i % len(key)]) ^ ord(char)) for i, char in enumerate(msg)])

plaintext = "Burning 'em, if you ain't quick and nimble"
plaintext2 = "I go crazy when I hear a cymbal"
key = "ICE"

print encrypt(key, plaintext + "\n" + plaintext2).encode("hex")
