import time
import random

secret_seed = int(time.time()) - random.randint(40, 1000) #simulate passage of time
random.seed(secret_seed)
secret_seed_output = random.random()

current_time = int(time.time())
cracked_seed = 0

for i in range(1001):
    random.seed(current_time - i)
    if random.random() == secret_seed_output:
        cracked_seed = current_time - i
        break

print secret_seed_output
print cracked_seed
print secret_seed == cracked_seed
