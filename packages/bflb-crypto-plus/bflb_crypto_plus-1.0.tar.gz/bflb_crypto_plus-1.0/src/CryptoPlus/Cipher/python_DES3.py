from .blockcipher import *
from . import pyDes

def new(key,mode=MODE_ECB,IV=None,counter=None,segment_size=None):
    """Create a DES-EDE3 or DES-EDE2 cipher object

    wrapper for pure python 3DES implementation pyDes.py

        key = raw string containing the 2/3 keys
            - DES-EDE2: supply 2 keys as 1 single concatenated 16byte key= key1|key2
            - DES-EDE3: supply 3 keys as 1 single concatenated 24byte key= key1|key2|key3
        mode = python_AES.MODE_ECB/CBC/CFB/OFB/CTR/CMAC, default is ECB
        IV = IV as a raw string, default is "all zero" IV
            -> only needed for CBC mode
        counter = counter object (CryptoPlus.Util.util.Counter)
            -> only needed for CTR mode
        segment_size = amount of bits to use from the keystream in each chain part
            -> supported values: multiple of 8 between 8 and the blocksize
               of the cipher (only per byte access possible), default is 8
            -> only needed for CFB mode

    EXAMPLES:
    **********
    IMPORTING:
    -----------
    >>> import codecs
    >>> from CryptoPlus.Cipher import python_DES3

    CBC TDES-EDE3 EXAMPLE: (using test vectors from http://csrc.nist.gov/groups/STM/cavp/documents/des/DESMMT.pdf)
    ------------
    >>> key = codecs.decode('37ae5ebf46dff2dc0754b94f31cbb3855e7fd36dc870bfae', 'hex')
    >>> IV = codecs.decode('3d1de3cc132e3b65', 'hex')
    >>> cipher = python_DES3.new(key, python_DES3.MODE_CBC, IV)
    >>> ciphertext = cipher.encrypt(codecs.decode('84401f78fe6c10876d8ea23094ea5309', 'hex'))
    >>> codecs.encode(ciphertext, 'hex')
    b'7b1f7c7e3b1c948ebd04a75ffba7d2f5'
    >>> decipher = python_DES3.new(key, python_DES3.MODE_CBC, IV)
    >>> plaintext = decipher.decrypt(ciphertext)
    >>> codecs.encode(plaintext, 'hex')
    b'84401f78fe6c10876d8ea23094ea5309'

    CMAC TDES-EDE3 EXAMPLE:
    -------------
    testvector: http://csrc.nist.gov/publications/nistpubs/800-38B/Updated_CMAC_Examples.pdf

    >>> key = codecs.decode('8aa83bf8cbda10620bc1bf19fbb6cd58bc313d4a371ca8b5', 'hex')
    >>> plaintext = codecs.decode('6bc1bee22e409f96e93d7e117393172aae2d8a57', 'hex')
    >>> cipher = python_DES3.new(key, python_DES3.MODE_CMAC)
    >>> codecs.encode(cipher.encrypt(plaintext), 'hex')
    b'743ddbe0ce2dc2ed'

    CMAC TDES-EDE2 EXAMPLE:
    -----------------------
    testvector: http://csrc.nist.gov/groups/STM/cavp/documents/mac/cmactestvectors.zip

    >>> key1 = codecs.decode("5104f2c76180c1d3", 'hex')
    >>> key2 = codecs.decode("b9df763e31ada716", 'hex')
    >>> key = key1 + key2
    >>> plaintext = codecs.decode('a6866be2fa6678f264a19c4474968e3f4eec24f5086d', 'hex')
    >>> cipher = python_DES3.new(key, python_DES3.MODE_CMAC)
    >>> codecs.encode(cipher.encrypt(plaintext), 'hex')
    b'32e7758f3f614dbf'"""
    return python_DES3(key,mode,IV,counter,segment_size)

class python_DES3(BlockCipher):
    key_error_message = "Key should be 128 or 192 bits"

    def __init__(self,key,mode,IV,counter,segment_size):
        cipher_module = pyDes.triple_des
        self.blocksize = 8
        BlockCipher.__init__(self,key,mode,IV,counter,cipher_module,segment_size)

    def keylen_valid(self,key):
        return len(key) in (16,24)

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
