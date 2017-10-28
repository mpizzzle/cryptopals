import re
from Crypto.Cipher import AES
from Crypto import Random

def random_key():
    return Random.new().read(AES.block_size)

key = random_key()

def encrypt(msg):
    pad_len = AES.block_size - (len(msg) % AES.block_size)
    return AES.new(key, AES.MODE_ECB).encrypt(msg + ''.join([chr(pad_len) for i in range(pad_len)]))

def decrypt_and_parse(cipher):
    return parse_string_to_dict(AES.new(key, AES.MODE_ECB).decrypt(cipher))

def parse_string_to_dict(token):
    return {entry.split('=')[0] : entry.split('=')[1] for entry in token.split('&')}

def profile_for(email):
    return encrypt("email=" + re.sub("[&|=]", '', email) + "&uid=10&role=user")

admin_cipher = profile_for("\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04admin\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04")
email_cipher = profile_for("michael770211@gmail.com\x04\x04\x04\x04\x04\x04")

print decrypt_and_parse(email_cipher[:AES.block_size * 3] + admin_cipher[AES.block_size : 2 * AES.block_size])
