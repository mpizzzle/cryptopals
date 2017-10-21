import re
from Crypto.Cipher import AES
from Crypto import Random

def random_key():
    return Random.new().read(AES.block_size)

key = random_key()

def encrypt(key, msg):
    return AES.new(key, AES.MODE_ECB).encrypt(msg + ''.join(['\x04' for i in range(AES.block_size - (len(msg) % AES.block_size      ))]) if len(msg) % AES.block_size != 0 else msg)

def decrypt_and_parse(key, cipher):
    return parse_string_to_dict(AES.new(key, AES.MODE_ECB).decrypt(cipher))

def parse_string_to_dict(token):
    return {entry.split('=')[0] : entry.split('=')[1] for entry in token.split('&')}

def profile_for(email):
    email_entry = "email=" + re.sub("[&|=]", '', email)
    cipher =  encrypt(key, email_entry)
    return decrypt_and_parse(key, cipher)

encoded_user_profile = "michael770211@gmail.com&uid=10&role=admin"
print profile_for(encoded_user_profile)
