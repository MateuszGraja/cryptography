import time
import hashlib

def measure_time(input_text, hash_function):
    start_time = time.time_ns()
    result = hash_function(input_text.encode())
    stop_time = time.time_ns()
    return (stop_time - start_time), result.hexdigest()


def main():
    input_text = input()
    md5_time,md5_result = measure_time(input_text, hashlib.md5)
    sha1_time,sha1_result = measure_time(input_text, hashlib.sha1)
    sha256_time,sha256_result = measure_time(input_text, hashlib.sha256)
    sha3_time,sha3_result = measure_time(input_text, hashlib.sha3_256)

    print(f"MD5 time: {md5_time} ns - result - {md5_result}")
    print(f"SHA-1 time: {sha1_time} ns - result {sha1_result}")
    print(f"SHA-2-256 time: {sha256_time} ns - result {sha256_result}")
    print(f"SHA-3-256 time: {sha3_time} ns - result {sha3_result}")
while True:
    main()