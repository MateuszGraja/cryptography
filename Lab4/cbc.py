from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def encrypt_cbc(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    block_size = AES.block_size
    cipher_ecb = AES.new(key, AES.MODE_ECB)
    pt = pad(plaintext, block_size)
    ciphertext = b""
    prev = iv
    for i in range(0, len(pt), block_size):
        block = pt[i:i+block_size]
        x = xor_bytes(block, prev)
        enc = cipher_ecb.encrypt(x)
        ciphertext += enc
        prev = enc
    return ciphertext

def decrypt_cbc(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    block_size = AES.block_size
    cipher_ecb = AES.new(key, AES.MODE_ECB)
    plaintext = b""
    prev = iv
    for i in range(0, len(ciphertext), block_size):
        block = ciphertext[i:i+block_size]
        dec = cipher_ecb.decrypt(block)
        pt_block = xor_bytes(dec, prev)
        plaintext += pt_block
        prev = block
    return unpad(plaintext, block_size)

if __name__ == "__main__":
    key = b"Sixteen byte key"
    iv  = b"Sixteen byte iv."
    msg = b"To jest testowa wiadomosc do zaszyfrowania w trybie CBC."
    ct = encrypt_cbc(msg, key, iv)
    print("Szyfrogram:", ct.hex())
    pt = decrypt_cbc(ct, key, iv)
    print("Odszyfrowano:", pt)
