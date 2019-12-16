#!/usr/bin/env python3
import requests

sid, url, auth = 1499734, 'http://131.155.21.174:8084', ('', 'please let me in')

req = requests.Session()

r = req.post(url+'/create', auth=auth, data={'sid': str(sid)}, allow_redirects=False)
ciphertext = bytes.fromhex(r.text.strip())

def oracle(cipher):
    assert hasattr(cipher,'hex') and len(cipher) % 16 == 0 and len(cipher) >= 32
    r = req.post(url+'/oracle', auth=auth, data={'cipher': cipher.hex()})
    return bool(['False', 'True'].index(r.text.strip()))

def validate(plaintext):  # use this to submit your plaintext once you've decrypted it
    assert type(plaintext) == str
    r = req.post(url+'/validate', auth=auth, data={'plaintext': plaintext})
    print('\x1b[32m{}\x1b[0m'.format(r.text.strip()))

################################################################

# let's try the oracle with a correct and invalid ciphertext.

res1 = oracle(ciphertext)
#test[16] = 0xaa
solution = []
for block_number in reversed(range(2,6)):
    print("block_number: "+str(block_number))
    modified_cipher = bytearray(ciphertext[(block_number-2)*16:block_number*16])
    original_cipher = bytearray(ciphertext[(block_number-2)*16:block_number*16])
    if block_number==5:
        start = 12
    else:
        start = 16
    for block_index in reversed(range(0,start)):
        print("block index: "+str(block_index))
        for padding_index in range(block_index+1,16):
            modified_cipher[padding_index] ^= 15-block_index
            modified_cipher[padding_index] ^= 16-block_index

        found_xor = 0
        for i in range(256):
            modified_cipher[block_index] = i
            if oracle(modified_cipher):
                found_xor = i
                break
                print(i)

        decrypted_value = (16-block_index) ^ found_xor
        solution = [chr(decrypted_value ^ original_cipher[block_index])] + solution
        #print(chr(decrypted_value ^ original_cipher[block_index]))
        print(solution)
        solution_string = ""
        for c in solution:
            solution_string += c
        print(solution_string)


validate(solution_string)
