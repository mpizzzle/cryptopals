from Crypto.Cipher import AES

def pkcs7_padding(msg):
    pad_len = AES.block_size - (len(msg) % AES.block_size)
    return msg + ''.join([chr(pad_len) for x in range(pad_len)])

def pkcs7_padding_stripper(msg):
    if ord(msg[len(msg) - 1]) > AES.block_size or ord(msg[len(msg) - 1]) == 0:
        raise Exception("invalid pkcs7 padding")
    for c in msg[len(msg) - ord(msg[len(msg) - 1]):]:
        if c != msg[len(msg) - 1]:
            raise Exception("invalid pkcs7 padding")
    return msg[:len(msg) - ord(msg[len(msg) - 1])]

plaintext = "YELLOW SUBMARINE"

pad = pkcs7_padding(plaintext)
print pad.encode("hex")
print pkcs7_padding_stripper(pad).encode("hex")
