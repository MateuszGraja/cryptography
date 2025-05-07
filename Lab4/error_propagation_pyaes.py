import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def count_byte_differences(a: bytes, b: bytes) -> int:
    return sum(1 for x, y in zip(a, b) if x != y) + abs(len(a) - len(b))

def propagate_error(mode_name: str, key: bytes, iv: bytes, nonce: bytes, data: bytes):
    print(f"\n=== {mode_name} ===")
    if mode_name == "ECB":
        enc = AES.new(key, AES.MODE_ECB)
        dec = AES.new(key, AES.MODE_ECB)
        pt = pad(data, AES.block_size)
    elif mode_name == "CBC":
        enc = AES.new(key, AES.MODE_CBC, iv)
        dec = AES.new(key, AES.MODE_CBC, iv)
        pt = pad(data, AES.block_size)
    elif mode_name == "OFB":
        enc = AES.new(key, AES.MODE_OFB, iv)
        dec = AES.new(key, AES.MODE_OFB, iv)
        pt = data
    elif mode_name == "CFB":
        enc = AES.new(key, AES.MODE_CFB, iv)
        dec = AES.new(key, AES.MODE_CFB, iv)
        pt = data
    elif mode_name == "CTR":
        n = nonce[:8]
        enc = AES.new(key, AES.MODE_CTR, nonce=n)
        dec = AES.new(key, AES.MODE_CTR, nonce=n)
        pt = data
    else:
        raise ValueError(f"Nieznany tryb: {mode_name}")

    ct = enc.encrypt(pt)

    corrupted = bytearray(ct)
    corrupted[5] ^= 0x01
    corrupted = bytes(corrupted)

    rec = dec.decrypt(corrupted)
    if mode_name in ("ECB", "CBC"):
        try:
            rec = unpad(rec, AES.block_size)
        except ValueError:
            pass

    diff = count_byte_differences(data, rec)
    print(f"Oryginał  : {data[:32]!r}... ({len(data)} bajtów)")
    print(f"Odszyfr.  : {rec[:32]!r}... ({len(rec)} bajtów)")
    print(f"Liczba zmienionych bajtów po błędzie w szyfrogramie: {diff}")

if __name__ == "__main__":
    data = (b"Wiadomosc testowa do zbadania propagacji bledow. " * 4)[:128]
    key   = os.urandom(16)
    iv    = os.urandom(16)
    nonce = os.urandom(16)

    for mode in ["ECB", "CBC", "OFB", "CFB", "CTR"]:
        propagate_error(mode, key, iv, nonce, data)
