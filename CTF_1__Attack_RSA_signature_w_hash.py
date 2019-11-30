#Authors: Job Douma & Maarten Dorrestijn
#Study: TRU/e Master Student Radboud University
#Course: Applied Crypto
#Assignment: CTF_1__Attack_RSA_Signatures_with_hash

#!/usr/bin/env python3
import sys, requests, re, hashlib, sympy, numpy as np, math

hashlen = 5

sid, url, auth = 1499734, 'http://78.47.101.119:8081', ('egal', 'please let me in')

sha = lambda m: int(hashlib.sha256((str(sid) + m).encode()).hexdigest()[:2*hashlen],16)

req = requests.Session()

r = req.post(url+'/create', auth=auth, data={'sid': str(sid)}, allow_redirects=False)
n,e = map(int, re.findall('[0-9]+', r.text))


def sign(m):
    r = req.post(url+'/sign', auth=auth, data={'msg': m})
    return int(r.text)

def validate(m, s):
    return pow(s, e, n) == sha(m)

def forgery(m, s):  # use this to submit your forgery once you've created it
    assert validate(m, s)
    r = req.post(url+'/validate_forgery', auth=auth, data={'msg': m, 'sig': str(s)})
    print('\x1b[32m{}\x1b[0m'.format(r.text.strip()))

def is_powersmooth(hash, primes):
    exponents = [0]*len(primes)
    i = 0
    while i<len(primes) and hash != 1:
        if hash % primes[i] == 0:
            hash = int(hash/primes[i])
            exponents[i] += 1
            i = 0
        else:
            i+=1
    if hash == 1:
        return exponents
    else:
        return False

#Extended Euclidean Algorithm
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

#Modulo Inverse
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

#Find Powersmooth values
def find_powersmooth():
    i=0
    j=0
    found_powersmooth = []
    while True:
        msg = str(i)
        if is_powersmooth(sha(msg),primes) != False:
            print("found!!!!!!!")
            print(msg)
            j+=1
            found_powersmooth.append(msg)
        if j==30:
            print(found_powersmooth)
            break
        i+=1

################################################################

print('public key: {}'.format((n,e)))

#step 1: let 𝑺=(𝒑_𝟏, . . . , 𝒑_𝒍) be the list of primes smaller than 𝒚.
primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71]

#step 2: Find at least 𝒍+𝟏 messages 𝑴_𝒊 such that each 𝛍(𝑴_𝒊)=(𝟎…𝟎||𝑯(𝑴_𝒊 )) is a product of primes in 𝑺 (i.e. 𝒚–smooth).
found_powersmooth = ['43179', '45413', '49714', '130985', '150654', '195251', '202500', '274083', '310753', '396278', '396326', '396387', '402878', '424954', '437061', '488578', '506955', '553183', '582536', '612773', '648975', '745593', '760534', '785356', '836642', '874922', '905619', '920391', '968124', '990312']

#step 3: Express one 𝛍(𝑴_𝒋 ) as a multiplicative combination of the other 𝛍(𝑴_𝒊 ) by solving a linear system given by the exponent vectors of the 𝛍(𝑴_𝒊 ) with respect to the primes in 𝑺.
vmod = []
for i in range(len(found_powersmooth)):
    vtmp = is_powersmooth(sha(found_powersmooth[i]),primes)
    for j in range(len(vtmp)):
        vtmp[j] = vtmp[j]%e
    vmod.append(vtmp)

mat = np.array(vmod[:21]) #dependent variable = 20th
echelon, inds = sympy.Matrix(mat).T.rref()

b = []
for i in range(len(echelon.col(-1))):#col(-1) gets last column
    p = echelon.col(-1)[i].p
    q = echelon.col(-1)[i].q
    b.append((p * pow(q, e-2, e)) % e)
print(b)

y = []
for i in range(20):
    s=0
    for j in range(20):
        nr = sympy.Matrix(mat).T.row(i) 
        s += nr[j]*b[j]
    y.append((-1*int(s/e)))
print(y)

#step 4: Ask for the signatures on all 𝑴_𝒊, 𝒊≠𝒋 and forge signature on 𝑴_𝒋.
#step 4.1: 𝝈* = 𝛍(𝑴_𝝉)^𝒅
#step 4.2: Compute:
#step 4.2.1: 𝝈* *= (∏_(𝒊=𝟏)^(𝝉−𝟏) ((𝛍(𝑴_𝒊)^𝒅)^(𝜷_𝒊)) 𝐦𝐨𝐝 𝑵
#step 4.2.2: 𝝈* *= (∏_(𝒋=𝟏)^𝒍 (𝒑_𝒋^(𝜸_𝒋))) 𝐦𝐨𝐝 𝑵
#step 4.3: Output forgery (𝝈*, 𝑴_𝝉)

sig = 1
for i in range(20):
    sig *= pow(sign(found_powersmooth[i]),b[i],n)
    sig %= n
for i in range(20):
    sig *= modinv(pow(primes[i],-1*y[i],n),n)
    sig %= n

message = found_powersmooth[20]
print('message: {}'.format(repr(message)))
print('signature: {}'.format(sig))
print('is valid? {}'.format(validate(message, sig)))
print('is valid? {}'.format(forgery(message, sig)))
print()

###########################################

#Signature validation serving as an example
msg = "Hi! Just trying this."
print('message: {}'.format(repr(msg)))

val = sha(msg)
print('hash value: {}'.format(val))

sig = sign(msg)
print('signature: {}'.format(sig))
print('is valid? {}'.format(validate(msg, sig)))