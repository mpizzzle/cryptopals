def _int32(x):
    # Get the 32 least significant bits.
    return int(0xffffffff & x)

class MT19937:
    def __init__(self, seed):
        # Initialize the index to 0
        self.index = 624
        self.mt = [0] * 624
        self.mt[0] = seed  # Initialize the initial state to the seed
        for i in range(1, 624):
            self.mt[i] = _int32(1812433253 * (self.mt[i - 1] ^ self.mt[i - 1] >> 30) + i)

    def set_state(self, cloned_state):
        self.mt = cloned_state 

    def extract_number(self):
        if self.index >= 624:
            self.twist()

        y = self.mt[self.index]

        # Right shift by 11 bits
        y = y ^ y >> 11
        # Shift y left by 7 and take the bitwise and of 2636928640
        y = y ^ y << 7 & 2636928640
        # Shift y left by 15 and take the bitwise and of y and 4022730752
        y = y ^ y << 15 & 4022730752
        # Right shift by 18 bits
        y = y ^ y >> 18

        self.index = self.index + 1

        return _int32(y)

    def twist(self):
        for i in range(624):
            # Get the most significant bit and add it to the less significant
            # bits of the next number
            y = _int32((self.mt[i] & 0x80000000) + (self.mt[(i + 1) % 624] & 0x7fffffff))
            self.mt[i] = self.mt[(i + 397) % 624] ^ y >> 1

            if y % 2 != 0:
                self.mt[i] = self.mt[i] ^ 0x9908b0df
        self.index = 0

def untemper_11(yy):
    y = yy ^ ((yy & 0xffe00000) >> 11)
    y = yy ^ ((y & 0xfffffc00) >> 11)
    y = yy ^ ((y & 0xffffffff) >> 11)
    
    return _int32(y)

def untemper_7(yy):
    y = yy ^ (((yy & 0x7f) << 7) & 2636928640)
    y = yy ^ (((y & 0x3fff) << 7) & 2636928640)
    y = yy ^ (((y & 0x1fffff) << 7) & 2636928640)
    y = yy ^ (((y & 0xfffffff) << 7) & 2636928640)
    y = yy ^ (((y & 0xffffffff) << 7) & 2636928640)

    return _int32(y)

def untemper_15(yy):
    y = yy ^ (((yy & 0x7fff) << 15) & 4022730752)
    y = yy ^ (((y & 0x3fffffff) << 15) & 4022730752)
    y = yy ^ (((y & 0xffffffff) << 15) & 4022730752)

    return _int32(y)

def untemper_18(yy):
    return _int32(yy ^ yy >> 18)

def untemper(yy):
    y = _int32(yy)
    y = untemper_18(y)
    y = untemper_15(y)
    y = untemper_7(y)
    y = untemper_11(y)
    return _int32(y)

unknown_seed = 12668778
mt = MT19937(unknown_seed)

cloned_mt_state = [0] * 624

for i in range(624):
    cloned_mt_state[i] = untemper(mt.extract_number())

cloned_mt = MT19937(0)
cloned_mt.set_state(cloned_mt_state)

print mt.extract_number()
print cloned_mt.extract_number()
print mt.extract_number() == cloned_mt.extract_number()
