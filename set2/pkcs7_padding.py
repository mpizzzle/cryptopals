def pkcs7_padding(block, block_length):
    return block + ''.join([chr(4) for x in range(block_length - len(block))])

block = "YELLOW SUBMARINE"

print pkcs7_padding(block, 32)
