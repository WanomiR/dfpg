import numpy as np
from colour import io, sRGB_to_XYZ, XYZ_to_Lab, XYZ_to_ProLab, ProLab_to_XYZ, XYZ_to_sRGB

from PIL import Image

vision250d_printed = io.convert_bit_depth(io.read_image("/Users/aleksejromadin/Desktop/SDIM1575.jpeg", "uint8"),
                                          "float32")


# colors=np.array(vision250d_printed)
# colors=colors.reshape((-1,3),)


def to_ProHsl(img):
    img = sRGB_to_XYZ(img)
    img = XYZ_to_ProLab(img)
    # vision250d_printed=io.convert_bit_depth(vision250d_printed,"uint16")
    L = (img[..., 0] / 100)
    a = (img[..., 1] / 128)
    b = (img[..., 2] / 128)
    # io.convert_bit_depth(L,"uint16")
    print(np.max(a))
    S = np.sqrt((a ** 2) + (b ** 2))
    H = np.arctan2(b, a)
    print(np.max(H), "    ", np.min(H))
    img = (np.stack((L, S, H), axis=-1))
    return img


hsl = to_ProHsl(vision250d_printed)


def from_ProHsl(img):
    L = img[..., 0]
    H = img[..., 2]
    S = img[..., 1]
    a2 = S * np.cos(H) * 128
    b2 = S * np.sin(H) * 128
    L *= 100
    img = (np.stack((L, a2, b2), axis=-1))
    img = ProLab_to_XYZ(img)
    img = XYZ_to_sRGB(img)
    print(L.shape)
    S = io.write_image(img, "/Users/aleksejromadin/Desktop/imajes/Sut.tiff", "uint16")
    return img


rgb = from_ProHsl(hsl)
