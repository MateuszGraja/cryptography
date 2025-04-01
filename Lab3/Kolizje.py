import hashlib
import random
import string

def generate_random_input(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def first_12_bits(md5_hash):
    return md5_hash[:3]

def test_collision(num_inputs=10000):
    seen = {}
    for _ in range(num_inputs):
        inp = generate_random_input()
        hash_val = hashlib.md5(inp.encode()).hexdigest()
        key = first_12_bits(hash_val)
        if key in seen:
            print(f"Kolizja: {key} dla {inp} oraz {seen[key]}")
            return
        seen[key] = inp
    print("Brak kolizji")

test_collision()