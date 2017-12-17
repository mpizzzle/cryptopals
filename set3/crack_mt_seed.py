import time
import random

class mersenne_twister:
    #Initialize the generator from a seed
    def __init__(self, seed):
        self.MT = [0] * 624
        self.MT[0] = seed
        self.index = 624
        for i in range(1, 624): #loop over each element
            self.MT[i] = int(0xFFFFFFFF & (1812433253 * (self.MT[i - 1] ^ (self.MT[i - 1] >> (30))) + i))

    #Extract a tempered value based on MT[index]
    #calling twist() every n numbers
    def extract_number(self):
        if self.index >= 624:
            if self.index > 624:
                raise Exception("Generator was never seeded")
                #Alternatively, seed with constant value; 5489 is used in reference C code[49]
            self.twist()

        y = self.MT[self.index]
        y = y ^ ((y >> 11) & 0xFFFFFFFF)
        y = y ^ ((y <<  7) & 0x9D2C5680)
        y = y ^ ((y << 15) & 0xEFC60000)
        y = y ^  (y >> 18)

        self.index += 1
        return int(0xFFFFFFFF & y)

    #Generate the next n values from the series x_i
    def twist(self):
        for i in range(624):
            x = int(0xFFFFFFFF & ((self.MT[i] & 0x80000000) + (self.MT[(i + 1) % 624] & 0x7fffffff)))
            xA = x >> 1

            if (x % 2) != 0: #lowest bit of x is 1
                xA = xA ^ 0x9908B0DF

            self.MT[i] = self.MT[(i + 397) % 624] ^ xA
        self.index = 0

secret_seed = int(time.time())
time.sleep(random.randint(40, 1000))
secret_seed_output = mersenne_twister(secret_seed).extract_number()
print secret_seed_output

current_time = int(time.time())
cracked_seed = 0

for i in range(1001):
    if mersenne_twister(current_time - i).extract_number() == secret_seed_output:
        cracked_seed = current_time - i
        break

print mersenne_twister(cracked_seed).extract_number()
print cracked_seed
print secret_seed == cracked_seed
