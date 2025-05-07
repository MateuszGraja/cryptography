import os
import time
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def measure_mode(file_path: str, key: bytes, iv: bytes, mode_name: str):
    with open(file_path, "rb") as f:
        plaintext = f.read()

    if mode_name == "ECB":
        encryptor = AES.new(key, AES.MODE_ECB)
        decryptor = AES.new(key, AES.MODE_ECB)
        pt = plaintext

    elif mode_name == "CBC":
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        decryptor = AES.new(key, AES.MODE_CBC, iv)
        pt = pad(plaintext, AES.block_size)

    elif mode_name == "CTR":
        nonce = iv[:8]
        encryptor = AES.new(key, AES.MODE_CTR, nonce=nonce)
        decryptor = AES.new(key, AES.MODE_CTR, nonce=nonce)
        pt = pad(plaintext, AES.block_size)

    else:
        raise ValueError(f"Nieznany tryb: {mode_name}")

    t0 = time.perf_counter()
    ciphertext = encryptor.encrypt(pt)
    t_enc = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    recovered = decryptor.decrypt(ciphertext)
    if mode_name in ("CBC", "CTR"):
        recovered = unpad(recovered, AES.block_size)
    t_dec = (time.perf_counter() - t0) * 1000

    return round(t_enc, 2), round(t_dec, 2)


def test_selected_modes(key: bytes, iv: bytes, files: list, modes: list):
    results = {m: {} for m in modes}
    for m in modes:
        for f in files:
            te, td = measure_mode(f, key, iv, m)
            results[m][os.path.basename(f)] = (te, td)
    return results


def plot_results(results: dict):
    file_sizes = [f.replace("file_", "").replace(".txt", "") for f in next(iter(results.values())).keys()]
    categories = []
    for sz in file_sizes:
        categories += [f"Szyfrowanie {sz}", f"Odszyfrowanie {sz}"]
    x = np.arange(len(categories))

    modes = list(results.keys())
    width = 0.2

    plt.figure(figsize=(10, 5))
    for i, m in enumerate(modes):
        vals = []
        for f in results[m]:
            te, td = results[m][f]
            vals += [te, td]
        offset = (i - (len(modes)-1)/2) * width
        plt.bar(x + offset, vals, width=width, label=m)

    plt.xticks(x, categories, rotation=45, ha="right")
    plt.ylabel("Czas w ms")
    plt.title("Czas szyfrowania i odszyfrowania plików .txt")
    plt.legend()
    plt.tight_layout()
    plt.savefig("wynik.png")
    print("Wykres zapisany do wynik.png")


if __name__ == "__main__":
    key = os.urandom(16)
    iv  = os.urandom(16)
    files = [
        "resources/file_1MB.txt",
        "resources/file_5MB.txt",
        "resources/file_10MB.txt"
    ]
    modes = ["ECB", "CBC", "CTR"]

    res = test_selected_modes(key, iv, files, modes)

    for mode, stats in res.items():
        print(f"--- {mode} ---")
        for fname, (te, td) in stats.items():
            print(f"{fname}: enc {te} ms, dec {td} ms")

    plot_results(res)
