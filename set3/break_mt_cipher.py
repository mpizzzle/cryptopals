from mt19937 import MersenneTwister
from random import Random
import time

r = Random()
key = r.randint(0, 0xffff)
known_msg = "This is a known plaintext"
prefixed_msg = ''.join([chr(r.randint(0, 0xff)) for i in range(r.randint(0, 1000))]) + known_msg

def encrypt(key, msg):
    mt = MersenneTwister(key)
    return ''.join([chr(ord(c) ^ (0xff & mt.extract_number())) for c in msg])

def generate_token(seed):
    mt = MersenneTwister(seed)
    return ''.join([chr(0xff & mt.extract_number()) for i in range(8)])

cipher = encrypt(key, prefixed_msg)

for i in range(0x10000):
    if encrypt(i, cipher)[len(cipher) - len(known_msg):] == known_msg:
        print i, i == key
        break

current_time = int(time.time())
token = generate_token(current_time)

for i in range(100):
    guessed_token = generate_token(current_time - i)
    if token == guessed_token:
        print True
        break
