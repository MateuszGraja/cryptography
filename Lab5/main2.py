#!/usr/bin/env python3
# visual_crypto_hardcoded.py

import random
from PIL import Image
import numpy as np

# → TUTAJ ustawiasz swoją ścieżkę do pliku:
IMAGE_PATH = "resources/img.jpg"

def przygotuj_obraz(path, size=(100, 100), prog=128):
    """
    Wczytuje obraz, scala do rozmiaru 100×100, konwertuje na odcienie szarości
    i binaruje (0=biały, 1=czarny).
    """
    img = Image.open(path).resize(size, Image.NEAREST).convert('L')
    arr = np.array(img)
    return (arr < prog).astype(np.uint8)

def generuj_podzialy(bin_img):
    """
    Generuje dwa udziały subpikselowe na bazie schematu 2-subpiksele poziomo.
    """
    h, w = bin_img.shape
    pod1 = np.zeros((h, w * 2), dtype=np.uint8)
    pod2 = np.zeros((h, w * 2), dtype=np.uint8)
    wzorce = [(1, 0), (0, 1)]

    for y in range(h):
        for x in range(w):
            pik = bin_img[y, x]
            wz = random.choice(wzorce)
            if pik == 0:
                # biały → oba identyczne
                pod1[y, 2*x:2*x+2] = wz
                pod2[y, 2*x:2*x+2] = wz
            else:
                # czarny → komplementarne
                pod1[y, 2*x:2*x+2] = wz
                pod2[y, 2*x]     = 1 - wz[0]
                pod2[y, 2*x+1]   = 1 - wz[1]
    return pod1, pod2

def zapisz_podzial(arr, filename):
    """
    Zapisuje tablicę subpikseli 0/1 jako obraz czarno-biały PNG.
    """
    img = Image.fromarray((1 - arr) * 255, 'L')
    img.save(filename)
    print(f">> zapisano: {filename}")

def zlacz_podzialy(p1_path, p2_path, out_path):
    """
    Składa udziały operacją OR i zapisuje wynik.
    """
    p1 = (np.array(Image.open(p1_path).convert('L')) < 128).astype(np.uint8)
    p2 = (np.array(Image.open(p2_path).convert('L')) < 128).astype(np.uint8)
    merged = (p1 | p2).astype(np.uint8)
    img = Image.fromarray((1 - merged) * 255, 'L')
    img.save(out_path)
    print(f">> złożony obraz: {out_path}")

# --- główny flow bez argumentów ---
binary = przygotuj_obraz(IMAGE_PATH)
share1, share2 = generuj_podzialy(binary)
zapisz_podzial(share1, "share_A.png")
zapisz_podzial(share2, "share_B.png")
zlacz_podzialy("share_A.png", "share_B.png", "recovered.png")
