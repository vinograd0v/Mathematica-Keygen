import random
import math

# Esta parte del código es del script de ibug.io, aunque allá está hecho en JS

def func1(n, abyte, c):
    for ibit in range(8):
        bit = (abyte >> ibit) & 1
        if bit + ((n - bit) & ~1) == n:
            n = (n - bit) >> 1
        else:
            n = ((c - bit) ^ n) >> 1
    return n

def generate_password(s, hash_val):
    for ibyte in range(len(s) - 1, -1, -1):
        hash_val = func1(hash_val, ord(s[ibyte]), 0x105C3)
    
    n1 = 0
    while func1(func1(hash_val, n1 & 0xFF, 0x105C3), n1 >> 8, 0x105C3) != 0xA5B6:
        if n1 >= 0xFFFF:
            return "Error"
        n1 += 1

    n1 = math.floor(((n1 + 0x72FA) & 0xFFFF) * 99999.0 / 0xFFFF)
    n1str = str(n1).zfill(5)

    temp = int(n1str[:-3] + n1str[-2:] + n1str[-3])
    temp = math.ceil((temp / 99999.0) * 0xFFFF)
    temp = func1(func1(0, temp & 0xFF, 0x1064B), temp >> 8, 0x1064B)

    for ibyte in range(len(s) - 1, -1, -1):
        temp = func1(temp, ord(s[ibyte]), 0x1064B)
    
    n2 = 0
    while func1(func1(temp, n2 & 0xFF, 0x1064B), n2 >> 8, 0x1064B) != 0xA5B6:
        if n2 >= 0xFFFF:
            return "Error"
        n2 += 1

    n2 = math.floor((n2 & 0xFFFF) * 99999.0 / 0xFFFF)
    n2str = str(n2).zfill(5)

    password = (
        n2str[3] + n1str[3] + n1str[1] + n1str[0] + '-' +
        n2str[4] + n1str[2] + n2str[0] + '-' +
        n2str[2] + n1str[4] + n2str[1] + "::1"
    )
    return password

def generate_password_from_id(mathId, activationKey, magic_number):
    password = generate_password(mathId + "$1&" + activationKey, magic_number)
    return password

# Algo importante es que los magicnumbers wolfram los puede  cambiar para  las nuevas versiones, entonces...
# El funcionamiento de esto depende de estarlos actualizando, pero en un principio debería durar.

def generate_wolfram_password(mathId="", activationKey=""):
    magicNumbers = [36412,24816,44011,33360,35944,59222] #https://github.com/thedeepdeepsky/mathematica_keygen
    keys_generated = 0
    for magic_number in magicNumbers:
        if keys_generated >= 5:
            break
        print(generate_password_from_id(mathId, activationKey, magic_number))
        keys_generated += 1

def generate_activation_key():
    random.seed()
    actkey = ''.join([str(random.randint(0, 9)) for _ in range(4)]) + '-'
    actkey += ''.join([str(random.randint(0, 9)) for _ in range(5)]) + '-'
    actkey += ''.join([str(random.randint(0, 9)) + chr(random.randint(65, 90)) for _ in range(3)])
    return actkey

if __name__ == "__main__":
    mathid = input("MathId: ")
    actkey = generate_activation_key()
    print("ActivationKey:", actkey)
    print("Possible passwords:")
    generate_wolfram_password(mathid, actkey)