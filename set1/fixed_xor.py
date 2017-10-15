import sys

key = "1c0111001f010100061a024b53535009181c"
msg = "686974207468652062756c6c277320657965"

print ''.join([chr(ord(a) ^ ord(b)) for a, b in zip(key.decode("hex"), msg.decode("hex"))]).encode("hex")
