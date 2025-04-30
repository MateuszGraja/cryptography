from PIL import Image
import numpy as np
import random

def generuj_udziały(obraz_path, rozmiar=(100, 100)):
    obraz = Image.open(obraz_path).convert("L")
    obraz = obraz.resize(rozmiar)
    obraz_np = np.array(obraz).astype(np.uint8)  # 0 = czarny, 255 = biały

    wysokosc, szerokosc = obraz_np.shape
    szerokosc_sub = szerokosc * 2  # poszerzamy obraz, bo piksel = 2 subpiksele

    # Udziały z subpikselami
    udzial1 = np.zeros((wysokosc, szerokosc_sub), dtype=np.uint8)
    udzial2 = np.zeros((wysokosc, szerokosc_sub), dtype=np.uint8)

    for i in range(wysokosc):
        for j in range(szerokosc):
            if obraz_np[i, j] == 255:  # biały piksel
                pattern = random.choice([[1, 0], [0, 1]])
                udzial1[i, 2*j] = pattern[0]
                udzial1[i, 2*j + 1] = pattern[1]
                udzial2[i, 2*j] = pattern[0]
                udzial2[i, 2*j + 1] = pattern[1]
            else:  # czarny piksel
                pattern1 = random.choice([[1, 0], [0, 1]])
                pattern2 = [1 - pattern1[0], 1 - pattern1[1]]
                udzial1[i, 2*j] = pattern1[0]
                udzial1[i, 2*j + 1] = pattern1[1]
                udzial2[i, 2*j] = pattern2[0]
                udzial2[i, 2*j + 1] = pattern2[1]

    udzial1_image = Image.fromarray((1 - udzial1) * 255, 'L')  # odwracamy: 0 → czarny
    udzial2_image = Image.fromarray((1 - udzial2) * 255, 'L')

    udzial1_image.save("udzial1.png")
    udzial2_image.save("udzial2.png")
    print("Udziały zostały zapisane jako 'udzial1.png' i 'udzial2.png'")

def zloz_udziały(udzial1_path, udzial2_path):
    udzial1 = Image.open(udzial1_path).convert("L")
    udzial2 = Image.open(udzial2_path).convert("L")

    udzial1_np = np.array(udzial1).astype(np.uint8) // 255
    udzial2_np = np.array(udzial2).astype(np.uint8) // 255

    wynik_np = udzial1_np | udzial2_np  # logiczne AND lub OR
    wynik_img = Image.fromarray((1 - wynik_np) * 255, 'L')

    wynik_img.save("wynik.png")
    print("Złożony obraz zapisano jako 'wynik.png'")

# Przykład użycia
obraz_path = "../resources/img.jpg"
generuj_udziały(obraz_path)
zloz_udziały("udzial1.png", "udzial2.png")
