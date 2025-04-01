import random
import math
from sympy import isprime

def generate_prime():
    lower, upper = 1000, 10000
    candidates = [p for p in range(lower, upper) if isprime(p)]
    return random.choice(candidates)

def find_prime(phi):
    while True:
        candidate = random.randint(2, phi - 1)
        if math.gcd(candidate, phi) == 1:
            return candidate

def main():
    p = generate_prime()
    q = generate_prime()

    n = p*q
    phi = (p-1)*(q-1)

    e = find_prime(phi) #public
    d = pow(e, -1, phi) #private

    message = "RSA klucz publiczny szyfrowanie i odszyfrowanie!!!"

    encrypted = [pow(ord(ch), e, n) for ch in message]
    print(f"encrypted: {encrypted}")

    decrypted = "".join(chr(pow(c, d, n)) for c in encrypted)
    print(f"decrypted: {decrypted}")

if __name__ == '__main__':
    main()