import numpy as np
from PIL import Image
import random

def tekst_to_bin(tekst: str) -> str:
    return ''.join(format(ord(i), '08b') for i in tekst)

def bin_to_tekst(bin_tekst: str) -> str:
    return ''.join(chr(int(bin_tekst[i:i+8], 2)) for i in range(0, len(bin_tekst), 8))

def watermark(image: Image.Image, key: int, tekst: str, n: int, d: int) -> Image.Image:
    np.random.seed(key)
    img_array = np.array(image, dtype=int)
    h, w, _ = img_array.shape

    bin_sekret = tekst_to_bin(tekst)
    sekret_index = 0
    sekret_len = len(bin_sekret)

    for _ in range(n):
        if sekret_index >= sekret_len:
            break

        y1, x1 = np.random.randint(0, h), np.random.randint(0, w)
        y2, x2 = np.random.randint(0, h), np.random.randint(0, w)

        img_array[y1, x1, 0] = (img_array[y1, x1, 0] & ~1) | int(bin_sekret[sekret_index])
        sekret_index += 1
        img_array[y2, x2, 0] = (img_array[y2, x2, 0] & ~1) | int(bin_sekret[sekret_index])
        sekret_index += 1

    return Image.fromarray(img_array.astype(np.uint8))

def watermark_detect(suspect: Image.Image, key: int, n: int, d: int, sekret_len: int) -> str:
    np.random.seed(key)
    img_array = np.array(suspect, dtype=int)

    bin_sekret = ''
    h, w, _ = img_array.shape
    sekret_index = 0

    for _ in range(n):
        if sekret_index >= sekret_len:
            break

        y1, x1 = np.random.randint(0, h), np.random.randint(0, w)
        y2, x2 = np.random.randint(0, h), np.random.randint(0, w)

        bin_sekret += str(img_array[y1, x1, 0] & 1)
        sekret_index += 1
        bin_sekret += str(img_array[y2, x2, 0] & 1)
        sekret_index += 1

    return bin_to_tekst(bin_sekret)

def main(path, tekst):
    image = Image.open(path)
    watermarked = watermark(image, key=1234, tekst=tekst, n=5000, d=100)
    watermarkpath = path.replace(".png", "_watermarked.png")
    watermarked.save(watermarkpath)

    odczytany_sekret = watermark_detect(watermarked, key=1234, n=5000, d=100, sekret_len=len(tekst_to_bin(tekst)))
    print(f"Odtworzony tekst z watermarku: {odczytany_sekret}")

    print(f"Oryginalny obraz:", watermark_detect(image, key=1234, n=5000, d=100, sekret_len=len(tekst_to_bin(tekst))))

tekst = "Ala ma kota"
main("Lab6/input.png", tekst)

tekst2 = "Tajny tekst"
main("Lab6/image.png", tekst2)
