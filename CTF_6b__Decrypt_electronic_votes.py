p = 146115460662583358579595245643269218399048931290498257266179149747095665757168965367610796236579513910320168650681429506079895131758419560837390775796137084325273935335744717696909616575920825594374133913703033153206366323678347485187546902380957772129651855649942758628796698850800771341743167728060677437107
q = (p-1)
g = 2
x = 79107368300770860699558137680812456062542328238291975581620300977068376639543379308625925374521249311631127876400870815804955451549943348184066318265344425846309510194054182942298071145919708171895694734561334573326396442614364124671541802389740903782689665240513300287609480949036359760332538917798703555443
i=0
l = ""
def legendre_symbol(a, p):
    """
    Legendre symbol
    Define if a is a quadratic residue modulo odd prime
    http://en.wikipedia.org/wiki/Legendre_symbol
    """
    ls = pow(a, (p - 1)//2, p)
    if ls == p - 1:
        return -1
    return ls

def prime_mod_sqrt(a, p):
    """
    Square root modulo prime number
    Solve the equation
        x^2 = a mod p
    and return list of x solution
    http://en.wikipedia.org/wiki/Tonelli-Shanks_algorithm
    """
    a %= p

    # Simple case
    if a == 0:
        return [0]
    if p == 2:
        return [a]

    # Check solution existence on odd prime
    if legendre_symbol(a, p) != 1:
        return []

    # Simple case
    if p % 4 == 3:
        x = pow(a, (p + 1)//4, p)
        return [x, p-x]

    # Factor p-1 on the form q * 2^s (with Q odd)
    q, s = p - 1, 0
    while q % 2 == 0:
        s += 1
        q //= 2

    # Select a z which is a quadratic non resudue modulo p
    z = 1
    while legendre_symbol(z, p) != -1:
        z += 1
    c = pow(z, q, p)

    # Search for a solution
    x = pow(a, (q + 1)//2, p)
    t = pow(a, q, p)
    m = s
    while t != 1:
        # Find the lowest i such that t^(2^i) = 1
        i, e = 0, 2
        for i in xrange(1, m):
            if pow(t, e, p) == 1:
                break
            e *= 2

        # Update next value to iterate
        b = pow(c, 2**(m - i - 1), p)
        x = (x * b) % p
        t = (t * b * b) % p
        c = (b * b) % p
        m = i

    return [x, p-x]

def get_mod4(val):
    tmpval = val
    mod2 = 0
    if pow(tmpval,q,p) != 1:
        mod2 = 1
        tmpval *= 2
    sqrt = prime_mod_sqrt(tmpval,p)[0]
    mod4 = 0
    print("pow:" + str(pow(sqrt,q,p)))
    if pow(sqrt,q,p) != 1:
        mod4 = 1

    print(mod4)
    print(mod2)
    return 2*mod4 + mod2
powlist = [pow(g,i*(q//13),p) for i in range(13)]
def get_mod13(x):
    return powlist.index(pow(x,q//13,p))
print("x: " + str(get_mod13(x)))
with open("op6b.txt") as f:
    for line in f:
        a = int(line.split(",")[0])
        b = int(line.split(",")[1])

        tmp = (get_mod13(b)-get_mod13(a))%13
        if tmp == 0:
            l += "Lorenz,"
        elif tmp == 9:
            l+="Andreas,"
        elif tmp == 10:
            l += "Florian,"
        elif tmp == 11:
            l += "Tanja,"
        else:
            print("Error!!!!!!!!!!!!!!!!")
        i+=1
print(i)
print(l)
