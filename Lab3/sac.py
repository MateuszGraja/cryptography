import hashlib

def hex_to_bin(hex_str):
    scale = 16
    num_of_bits = len(hex_str) * 4
    return bin(int(hex_str, scale))[2:].zfill(num_of_bits)

def sac_test(input_text, hash_function):
    original_hash = hash_function(input_text.encode()).hexdigest()
    original_bin = hex_to_bin(original_hash)

    altered_text = list(input_text)
    if altered_text:
        altered_text[0] = chr((ord(altered_text[0]) + 1) % 256)
    altered_text = ''.join(altered_text)

    altered_hash = hash_function(altered_text.encode()).hexdigest()
    altered_bin = hex_to_bin(altered_hash)

    differences = sum(1 for b1, b2 in zip(original_bin, altered_bin) if b1 != b2)
    total_bits = len(original_bin)
    ratio = differences / total_bits
    print(f"Zmiana {differences} bitów na {total_bits} (stosunek {ratio:.2f})")

sac_test("Kot", hashlib.sha256)
