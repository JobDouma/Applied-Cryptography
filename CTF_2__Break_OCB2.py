#Authors: Job Douma & Maarten Dorrestijn
#Study: TRU/e Master Student Radboud University
#Course: Applied Crypto
#Assignment: CTF_2__Break_OCB2

#!/usr/bin/env python3
import requests
from random import randint

sid, url, auth = 1499734, 'http://131.155.21.174:8082', ('', 'please let me in')

req = requests.Session()

r = req.post(url+'/create', auth=auth, data={'sid': str(sid)}, allow_redirects=False)

def encrypt(nonce, plain):
    assert hasattr(nonce,'hex') and hasattr(plain,'hex') and len(nonce) == 16
    r = req.post(url+'/encrypt', auth=auth, data={'nonce': nonce.hex(), 'plain': plain.hex()})
    return tuple(map(bytes.fromhex, r.text.strip().split()))

def decrypt(nonce, cipher, tag):
    assert hasattr(nonce,'hex') and hasattr(cipher,'hex') and hasattr(tag,'hex') and len(nonce) == len(tag) == 16
    r = req.post(url+'/decrypt', auth=auth, data={'nonce': nonce.hex(), 'cipher': cipher.hex(), 'tag': tag.hex()})
    if 'INVALID' in r.text: return
    return bytes.fromhex(r.text.strip())

def forgery(nonce, cipher, tag):  # use this to submit your forgery once you've created it
    assert type(nonce) == type(cipher) == type(tag) == bytes
    assert len(cipher) >= 33 and len(nonce) == len(tag) == 16
    r = req.post(url+'/validate_forgery', auth=auth, data={'nonce': nonce.hex(), 'cipher': cipher.hex(), 'tag': tag.hex()})
    print('\x1b[32m{}\x1b[0m'.format(r.text.strip()))

def xor(xs,ys):
    assert len(xs) == len(ys) == 16
    return bytes(x^y for x,y in zip(xs,ys))
################################################################

# let's encrypt a plaintext and try decrypting a correct and invalid ciphertext.

nonce = bytes("{:<16}".format(str(randint(0,10000))),'utf-8')
message = (b'\x00'*32)+b'\x00'*15+b'\x80' + b'\x00'*16
print(len(message))
cipher,tag = encrypt(nonce,message)

print(cipher)
m=4
forgedcipher = bytearray((m-1)*16)
forgedcipher[32:48] = xor(cipher[32:48], b'\x00'*15+b'\x80')

forgedcipher[0:32] = cipher[0:32]
forgedtag =  xor(cipher[48:64], message[48:64])
forgedcipher = bytes(forgedcipher)
print(forgedcipher)
forgery(nonce, forgedcipher, forgedtag)
print(forgedcipher)
print(decrypt(nonce, forgedcipher, forgedtag))







################################################################

'''
    In case you're bored, you can use the following helper functions to
    create universal forgeries and decrypt our challenge ciphertext.
    No extra credit, though.
'''


# convert a number in [0..2^128) to a 16-byte block
def n2b(n):
    assert 0 <= n < 2**128
    return int.to_bytes(n, 16, 'big')

# convert a 16-byte block to a number in [0..2^128)
def b2n(b):
    assert len(b) == 16
    return int.from_bytes(b, 'big')

# XOR two 16-byte blocks


ffpoly = sum(1<<i for i in (0,1,2,7,128))

# multiplication in OCB2's finite field
def ffmul(x,y, r=0):
    while y:
        if y&1: r ^= x
        x <<= 1
        if x&(1<<128): x ^= ffpoly
        y >>= 1
    return r

# exponentiation in OCB2's finite field
def ffexp(x,n):
    if n < 0: return exp(inv(x),-n)
    r = 1
    while n:
        if n&1: r = mul(r,x)
        x = mul(x,x)
        n >>= 1
    return r

# inversion in OCB2's finite field
def ffinv(x):
    y = exp(x, 2**128-2)
    assert mul(x,y)==1
    return y