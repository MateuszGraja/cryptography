#Lab 1
import math
import random
from sympy import isprime


def generate_prime():
    min_val = 1001
    max_val = 10000
    candidates = [num for num in range(min_val, max_val, 2) if isprime(num) and num % 4 == 3]
    return random.choice(candidates)

def relatively_prime(N):
    rel_pr = random.randrange(2,N)

    while math.gcd(rel_pr, N) != 1:
        rel_pr = random.randrange(2,N)

    return rel_pr

def monobit_test(bits):
    ones = sum(bits)
    lower, upper = 9725, 10275
    result = lower < ones < upper
    return result

def extended_series(bits):
    max_run = 1
    current_run = 1
    for i in range(1, len(bits)):
        if bits[i] == bits[i-1]:
            current_run += 1
        else:
            if current_run > max_run:
                max_run = current_run
            current_run = 1
    max_run = max(current_run, max_run)
    result = max_run < 26
    return result

def series(bits):
    counter = 0
    intervals = [
        [2315, 2685],
        [1114, 1386],
        [527, 723],
        [240, 384],
        [103, 209],
        [103, 209],
    ]

    series_zeros = [0 for _ in range(6)]
    series_ones = [0 for _ in range(6)]
    for i in range(len(bits) - 2):
        counter += 1
        if bits[i + 1] != bits[i]:
            if counter <= 5:
                if bits[i] == 0:
                    series_zeros[counter - 1] += 1
                else:
                    series_ones[counter - 1] += 1
                counter = 0
            else:
                if bits[i] == 0:
                    series_zeros[5] += 1
                else:
                    series_ones[5] += 1

                counter = 0
    for i in range(6):
        if not (
                series_ones[i] <= intervals[i][1]
                and series_ones[i] >= intervals[i][0]
                and series_zeros[i] <= intervals[i][1]
                and series_zeros[i] >= intervals[i][0]
        ):
            return False
    return True

def poker_test(bits):
    m = 4
    n = len(bits) // m
    counts = [0]*16
    for i in range(n):
        segment = bits[i*m:(i+1)*m]
        value = segment[0]*8 + segment[1]*4 + segment[2]*2 + segment[3]
        counts[value] += 1
    X = (16 / n) * sum(c**2 for c in counts) - n
    result = 2.16 < X < 46.17
    return result


def main():
    p = generate_prime()
    q = generate_prime()

    while p==q:
        q = generate_prime()

    N = p*q

    relative_prime = relatively_prime(N)
    # print(N, relative_prime)

    #generacja ciągu 20 000 bitów
    x = pow(relative_prime, 2, N)
    bits = []
    for i in range(20000):
        x = pow(x, 2, N)
        bit = x & 1
        bits.append(bit)


    #TESTS
    print(f"monobit_test: {monobit_test(bits)}")
    print(f"extended_series: {extended_series(bits)}")
    print(f"series: {series(bits)}")
    print(f"poker_test: {poker_test(bits)}")





if __name__ == '__main__':
    main()