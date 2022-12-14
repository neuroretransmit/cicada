#!/usr/bin/env python3

from PIL import Image

def get_modified_bits(cicada, original, operation="xor"):
    width, height = cicada.size
    cicada_map = cicada.load()
    original_map = original.load()
    for i in range(width):
        for j in range(height):
            cr, cg, cb = cicada.getpixel((i, j))
            _or, og, ob = original.getpixel((i, j))
            if operation == "xor":
                cicada_map[i, j] = (cr ^ _or, cg ^ og, cb ^ ob)
            elif operation == "nand":
                cicada_map[i, j] = (cr if not (cr and _or) else 255, cg if not (cg and og) else 255, cb if not (cb and ob) else 255)
    cicada.save(f"{operation}.png", format="png")


cicada = Image.open("./q4utgdi2n4m4uim5.onion.jpeg")
original = Image.open("Francisco_de_Goya_y_Lucientes_-_Portrait_of_Andrés_del_Peral_-_WGA10031.jpg")
for op in ["xor", "nand"]:
    get_modified_bits(cicada, original, operation=op)
