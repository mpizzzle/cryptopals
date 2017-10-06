import sys

hex = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

for x in range(128):
	plaintext = ''.join([chr(x ^ ord(a)) for a in hex.decode("hex")])
	if " a " in plaintext:
		print plaintext