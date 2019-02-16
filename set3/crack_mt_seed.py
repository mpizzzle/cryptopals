import time
import random
from mt19937 import MersenneTwister

secret_seed = int(time.time())
time.sleep(random.randint(40, 1000))
secret_seed_output = MersenneTwister(secret_seed).extract_number()
print secret_seed_output

current_time = int(time.time())
cracked_seed = 0

for i in range(1001):
    if MersenneTwister(current_time - i).extract_number() == secret_seed_output:
        cracked_seed = current_time - i
        break

print MersenneTwister(cracked_seed).extract_number()
print cracked_seed
print secret_seed == cracked_seed
