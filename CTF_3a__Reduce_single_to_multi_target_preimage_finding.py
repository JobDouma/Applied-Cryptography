#Authors: Job Douma & Maarten Dorrestijn
#Study: TRU/e Master Student Radboud University
#Course: Applied Crypto
#Assignment: CTF_3a__Reduce_single_to_multi_target_preimage_finding

#!/usr/bin/env python3
import sys, requests, re, random, os

sid, url, auth = 1499734, 'http://131.155.21.174:8083', ('', 'please let me in')

req = requests.Session()

r = req.post(url+'/create', auth=auth, data={'sid': str(sid)}, allow_redirects=False)
target = bytes.fromhex(re.search('((?:[0-9a-f]{2})+)', r.text).groups()[0])

def hash(x):
    r = req.post(url+'/hash', auth=auth, data={'data': x.hex()})
    return bytes.fromhex(r.text)

def multi_unhash(xs):
    r = req.post(url+'/multi_unhash', auth=auth, data={'hashes': [x.hex() for x in xs]})
    r = r.text.strip().split()
    if r[1] == 'None': return int(r[0]), None  # bad query
    return int(r[0]), bytes.fromhex(r[1])

def preimage(x):  # use this to submit your preimage
    r = req.post(url+'/validate_preimage', auth=auth, data={'data': x.hex()})
    print('\x1b[32m{}\x1b[0m'.format(r.text.strip()))

################################################################

print('target hash value: {}'.format(target.hex()))

# let's compute a few hash values for fun

for _ in range(100):
    xs = []
    for _ in range(3):
        x = os.urandom(random.randrange(5,20))
        xs.append(hash(x))
    xs.append(target)
    for _ in range(6):
        x = os.urandom(random.randrange(5,20))
        xs.append(hash(x))
    index,preimage_output = multi_unhash(xs)
    if index==3:
        preimage(preimage_output)
