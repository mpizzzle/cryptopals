def _int32(x):
    # Get the 32 least significant bits.
    return int(0xFFFFFFFF & x)

class MT19937:

    def __init__(self, seed):
        # Initialize the index to 0
        self.index = 624
        self.mt = [0] * 624
        self.mt[0] = seed  # Initialize the initial state to the seed
        for i in range(1, 624):
            self.mt[i] = _int32(1812433253 * (self.mt[i - 1] ^ self.mt[i - 1] >> 30) + i)

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
            y = _int32((self.mt[i] & 0x80000000) +
                       (self.mt[(i + 1) % 624] & 0x7fffffff))
            self.mt[i] = self.mt[(i + 397) % 624] ^ y >> 1

            if y % 2 != 0:
                self.mt[i] = self.mt[i] ^ 0x9908b0df
        self.index = 0

def test_temper(yy):
        y = _int32(yy)
        y = y ^ y >> 11
        #y = y ^ y << 7 & 2636928640
        #y = y ^ y << 15 & 4022730752
        y = y ^ y >> 18
        return _int32(y)

def untemper_11(yy):
        y = _int32(yy)
        print format(y, '#034b')
        temp1 = y >> (32 - 11)
        print format(temp1, '#034b')
        temp2 = (y & 0x1fffff) >> (32 - 11 - 11)
        print format(temp2, '#034b')
        temp3 = temp1 ^ temp2# >> 1
        print format(temp3, '#034b')
        temp4 = int(str(format(temp1, '#011b')) + str(format(temp3, '011b')), 2) >> 1
        print format(temp4, '#034b')
        temp5 = temp4 ^ y
        print format(temp5, '#034b')
        return _int32(temp5)

def untemper_18(yy):
        y = _int32(yy)
        print format(y, '#034b')
        temp1 = y >> (32 - 11)
        print format(temp1, '#034b')
        temp2 = (y & 0x1fffff) >> (32 - 11 - 11)
        print format(temp2, '#034b')
        temp3 = temp1 ^ temp2# >> 1
        print format(temp3, '#034b')
        temp4 = int(str(format(temp1, '#011b')) + str(format(temp3, '011b')), 2) >> 1
        print format(temp4, '#034b')
        temp5 = temp4 ^ y
        print format(temp5, '#034b')
        return _int32(temp5)

def test_untemper(yy):
        y = _int32(yy)
        y = untemper_18(y)
        #y = y ^ y << 15 & 4022730752
        #y = y ^ y << 7 & 2636928640
        y = untemper_11(y)
        return _int32(y)

print _int32(48762549)
print _int32(48762549) == test_untemper(test_temper(48762549))
