from PIL import Image

def encode_lsb(image_path, message, output_path):
    img = Image.open(image_path).convert('RGB')
    byte_message = message.encode('utf-8') + b'\xFF\xFE\xFD'
    binary_message = ''.join(format(byte, '08b') for byte in byte_message)

    pixels = list(img.getdata())
    flat_pixels = [value for pixel in pixels for value in pixel]

    for i in range(len(binary_message)):
        flat_pixels[i] = (flat_pixels[i] & ~1) | int(binary_message[i])

    new_pixels = list(zip(*[iter(flat_pixels)]*3))
    img.putdata(new_pixels)
    img.save(output_path)
    print(f"Wiadomość została ukryta w {output_path}.")


def decode_lsb(image_path):
    img = Image.open(image_path).convert('RGB')
    pixels = list(img.getdata())
    bits = [color & 1 for pixel in pixels for color in pixel]
    bytes_data = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for bit in bits[i:i+8]:
            byte = (byte << 1) | bit
        bytes_data.append(byte)
        if bytes_data[-3:] == b'\xFF\xFE\xFD':
            break

    message = bytes_data[:-3].decode('utf-8')
    print("Odczytana wiadomość:", message)
    return message


with open("Lab7/pantadeusz.txt", "r", encoding="utf-8") as f:
    message = f.read().replace('\n', ' ')

encode_lsb("Lab7/image.png", message, "encoded.png")

output = decode_lsb("encoded.png")
with open("wiadomosc.txt", "w", encoding="utf-8") as f:
    f.write(output)