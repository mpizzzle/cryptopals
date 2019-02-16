from mt19937 import MersenneTwister

def _int32(x):
    # Get the 32 least significant bits.
    return int(0xffffffff & x)

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
mt = MersenneTwister(unknown_seed)

cloned_mt_state = [0] * 624

for i in range(624):
    cloned_mt_state[i] = untemper(mt.extract_number())

cloned_mt = MersenneTwister(0)
cloned_mt.set_state(cloned_mt_state)

print mt.extract_number()
print cloned_mt.extract_number()
print mt.extract_number() == cloned_mt.extract_number()
