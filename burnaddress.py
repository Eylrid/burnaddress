'''
*** WARNING *** WARNING *** WARNING *** WARNING ***

This script creates addresses that are unspendable!
Don't send any bitcoin to any addresses created by
this unless you want to burn them!

*** WARNING *** WARNING *** WARNING *** WARNING ***
'''

import hashlib, math

CODESTRING = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

class ChecksumError(Exception):
    '''Raised when a checksum fails'''
    pass

def sha256(s):
    return hashlib.sha256(s).digest()

def doublehash(s):
    return sha256(sha256(s))

def checksum(s):
    return doublehash(s)[:4]

def bytes_to_int(s):
    '''Takes a byte string and converts it to an integer using big endian.'''
    return int(s.encode('hex'), 16)

def int_to_bytes(n):
    '''
    Takes an integer and converts it to an unsigned big endian byte string.
    '''
    h = hex(n)[2:]
    if h.endswith('L'): h = h[:-1]
    if len(h)%2 == 1:
        #odd length hex string, prepend 0
        h = '0'+h

    return h.decode('hex')

def encode_base_58(s):
    '''Encode a byte string in base-58'''
    x = bytes_to_int(s)
    result = ''
    while(x>0):
        x, remainder = x/58, x%58
        result += CODESTRING[remainder]

    while s.startswith('\x00'):
        result += CODESTRING[0]
        s = s[1:]

    return result[::-1]

def decode_base_58(base58):
    '''Decode a base58 string'''
    n = 0
    for c in base58:
        index = CODESTRING.index(c)
        n = n*58 + index

    result = int_to_bytes(n)

    while base58.startswith(CODESTRING[0]):
        result = '\x00' + result
        base58 = base58[1:]

    return result

def encode_base_58_check(s):
    '''Take a string (including version) and return a base58check'''
    bytes = s
    check = checksum(bytes)
    bytes += check
    return encode_base_58(bytes)

def decode_base_58_check(base58check):
    '''
    Decode and verify a base58check string

    returns (version, decoded string)'''
    bytes = decode_base_58(base58check)
    check, bytes = bytes[-4:], bytes[:-4]
    if checksum(bytes) != check: raise ChecksumError('invalid checksum')
    return bytes[0], bytes[1:]

def base58_to_base58check(base58, prepend='EJ'):
    '''Take a base58 encoded string and turn it into a base58check'''
    padchar = CODESTRING[len(CODESTRING)/2]
    base58 = prepend + base58 + padchar*6        # pad base58 to give room for checksum
    bytes = decode_base_58(base58)
    if len(bytes) < 25:
        # pad to get valid address length
        base58 = base58 + padchar*int(((25-len(bytes))*math.log(256.)/math.log(58.)))
        bytes = decode_base_58(base58)
        if len(bytes) < 25:
            # still not long enough
            base58 += padchar
            bytes = decode_base_58(base58)

    assert len(bytes) == 25

    bytes = bytes[:-4]                        # remove checksum bytes
    return encode_base_58_check(bytes)

if __name__ == '__main__':
    s = raw_input('String? ')
    warning = 'WARNING! This address cannot be spent from! WARNING!'
    print
    print warning
    print
    print base58_to_base58check(s)
    print
    print warning
