from PIL import Image
import numpy as np
import random

def generuj_udzialy(obraz_path='resources/img.jpg', rozmiar=(100, 100)):
    # Wczytaj obraz i skaluj
    obraz = Image.open(obraz_path).convert('L')
    obraz = obraz.resize(rozmiar)
    arr = np.array(obraz, dtype=np.uint8)

    h, w = arr.shape
    w2 = w * 2  # każdy piksel → 2 subpiksele

    udzial1 = np.zeros((h, w2), dtype=np.uint8)
    udzial2 = np.zeros((h, w2), dtype=np.uint8)

    patterns = [[1, 0], [0, 1]]

    for i in range(h):
        for j in range(w):
            p = random.choice(patterns)
            if arr[i, j] == 255:  # biały piksel
                # oba udziały mają ten sam wzór
                udzial1[i, 2*j:2*j+2] = p
                udzial2[i, 2*j:2*j+2] = p
            else:  # czarny piksel
                # wzory komplementarne
                udzial1[i, 2*j:2*j+2] = p
                udzial2[i, 2*j:2*j+2] = [1-p[0], 1-p[1]]

    def to_image(a):
        # 1 → biały (255), 0 → czarny (0)
        return Image.fromarray((1 - a) * 255, mode='L')

    to_image(udzial1).save('udzial1.png')
    to_image(udzial2).save('udzial2.png')
    print("Zapisano: udzial1.png, udzial2.png")


def zloz_udzialy(p1='udzial1.png', p2='udzial2.png'):
    u1 = Image.open(p1).convert('L')
    u2 = Image.open(p2).convert('L')

    a1 = (np.array(u1) // 255).astype(np.uint8)
    a2 = (np.array(u2) // 255).astype(np.uint8)

    res = a1 | a2
    Image.fromarray((1 - res) * 255, mode='L').save('wynik.png')
    print("Zapisano: wynik.png")


if __name__ == '__main__':
    generuj_udzialy()
    zloz_udzialy()
