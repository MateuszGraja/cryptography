import random
from sympy import isprime, primerange

def generate_prime():
    lower, upper = 1000, 10000
    candidates = [p for p in range(lower, upper) if isprime(p)]
    return random.choice(candidates)

def find_primitive_root(n):
    factors = list(primerange(2, n - 1))
    for g in range(2, n):
        flag = True
        for factor in factors:
            if pow(g, (n - 1) // factor, n) == 1:
                flag = False
                break
        if flag:
            return g
    return None


def main():
    n = generate_prime()
    g = find_primitive_root(n)
    print(n, g)

    #tajny klucz A, B
    x = random.randint(2, n - 2)
    y = random.randint(2, n - 2)

    X = pow(g, x, n)
    Y = pow(g, y, n)

    kA = pow(Y, x, n)
    kB = pow(X, y, n)
    print(f"Klucz k: {kA} oraz {kB}")

if __name__ == '__main__':
    main()
