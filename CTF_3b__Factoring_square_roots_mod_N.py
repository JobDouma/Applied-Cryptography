#Authors: Job Douma & Maarten Dorrestijn
#Study: TRU/e Master Student Radboud University
#Course: Applied Crypto
#Assignment: CTF_3b__Factoring_square_roots_mod_N

#!/usr/bin/env python3
import sys, requests, re, random,  math


sid, url, auth = 1499734, 'http://131.155.21.174:8183', ('', 'please let me in')

req = requests.Session()

r = req.post(url+'/create', auth=auth, data={'sid': str(sid)}, allow_redirects=False)
n = int(*re.findall('[0-9]+', r.text))


def sqrt(x):
    r = req.post(url+'/sqrt', auth=auth, data={'value': x})
    if r.text.strip() == 'None': return None  # not a square
    return int(r.text)

def factorization(p, q):  # use this to submit your factorization
    assert type(p) == type(q) == int
    r = req.post(url+'/validate_factorization', auth=auth, data={'p': '{:d}'.format(p), 'q': '{:d}'.format(q)})
    print('\x1b[32m{}\x1b[0m'.format(r.text.strip()))
def hcfnaive(a,b):
    if(b==0):
        return a
    else:
        return hcfnaive(b,a%b)
def gcd(x, y):
    while y != 0:
        (x, y) = (y, x % y)
    return x
################################################################

print('n: {}'.format(n))

# let's compute a few square roots for fun

for _ in range(10000):
    x = random.randrange(n)
    y = sqrt((x*x)%n)

    print(x)
    print(y)
    print()
    if y != x:
        print("found!")
        p = gcd(x-y,n)
        q =  n//p
        print("n:\t"+str(int(p*q)))
        print("p:\t"+str(p))
        print("q:\t"+str(q))
        print()
        print(int(n-(p*q)))
        factorization(p,q)
        break