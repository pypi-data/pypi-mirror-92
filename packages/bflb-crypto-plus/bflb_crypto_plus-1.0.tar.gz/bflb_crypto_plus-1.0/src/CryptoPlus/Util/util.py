import binascii
def number2string(i):
    """Convert a number to a string

    Input: long or integer
    Output: string (big-endian)
    """
    s=hex(i)[2:].rstrip('L')
    if len(s) % 2:
        s = '0' + s
    return binascii.unhexlify(s)

def number2string_N(i, N):
    """Convert a number to a string of fixed size

    i: long or integer
    N: length of string
    Output: string (big-endian)
    """
    s = '%0*x' % (N*2, i)
    return binascii.unhexlify(s)

def string2number(i):
    """ Convert a string to a number

    Input: string (big-endian)
    Output: long or integer
    """
    return int(binascii.hexlify(i),16)

def xorstring(a,b):
    """XOR two strings of same length

    For more complex cases, see CryptoPlus.Cipher.XOR"""
    #print(a)
    #print(b)
    assert len(a) == len(b)
    return number2string_N(string2number(a)^string2number(b), len(a))

class Counter(str):
    #found here: http://www.lag.net/pipermail/paramiko/2008-February.txt
    """Necessary for CTR chaining mode

    Initializing a counter object (ctr = Counter('xxx'), gives a value to the counter object.
    Everytime the object is called ( ctr() ) it returns the current value and increments it by 1.
    Input/output is a raw string.

    Counter value is big endian"""
    def __init__(self, initial_ctr):
        if not isinstance(initial_ctr, bytes):
            raise TypeError("nonce must be bytes")
        self.c = int(binascii.hexlify(initial_ctr), 16)
    def __call__(self):
        # This might be slow, but it works as a demonstration
        ctr = binascii.unhexlify("%032x" % (self.c,))
        self.c += 1
        return ctr

