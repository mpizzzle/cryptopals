from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util import Counter

frequent_letters = "etaoishr ETAOISHR"
key = Random.new().read(AES.block_size)

def encrypt(plaintext):
    return AES.new(key, AES.MODE_CTR, counter=Counter.new(128)).encrypt(plaintext)

def decrypt(key, msg):
    return ''.join([chr(ord(key[i % len(key)]) ^ ord(char)) for i, char in enumerate(msg)])

def get_candidate_key_byte(transposed_block):
    candidate = ''
    candidate_frequency = 0

    for c in range(256):
        plaintext = ''.join([chr(c ^ ord(a)) for a in transposed_block])
        frequency = sum([plaintext.count(frequent_letters[n]) for n in range(len(frequent_letters))])

        if frequency > candidate_frequency:
            candidate = chr(c)
            candidate_frequency = frequency

    return candidate

def get_key(file, key_length):
    split_file = [file[i:i + key_length] for i in range(0, len(file), key_length)]
    transposed_blocks = [''.join([block[x] for block in split_file[:len(split_file) - 1]]) for x in range(key_length)]
    return ''.join([get_candidate_key_byte(block) for block in transposed_blocks])

with open('files/20.txt') as f:
    ciphertexts = [encrypt(line.decode("base64")) for line in f.read().splitlines()]

key_length = min(len(ct) for ct in ciphertexts)
ciphertext = ''.join([ct[:key_length] for ct in ciphertexts])
plaintext = decrypt(get_key(ciphertext, key_length), ciphertext)

for line in [plaintext[i:i + key_length] for i in range(0, len(plaintext), key_length)]:
    print line
