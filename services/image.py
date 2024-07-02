import numpy as np
from PIL import Image


PIXEL_SIZE_BITS = 32
NUM_VALUES_PER_PIXEL = 4


def int_to_bits(integer: np.ndarray):
    return ((integer.reshape(-1, 1) & (1 << np.arange(8))) != 0).astype(int)[:, ::-1]


def bits_to_int(bits):
    return (bits * (1 << np.arange(8)[::-1])).sum(axis=1)


def get_image_data(input_path: str):
    with Image.open(input_path) as image:
        data = np.array(image.getdata(), dtype=np.uint8)
        data_bits = int_to_bits(data).reshape(-1)
        
    return data_bits


def put_image_data(input_path: str, output_path: str, encrypted_data):
    encrypted_data = encrypted_data.reshape(-1, PIXEL_SIZE_BITS)

    rgba_values = (
        bits_to_int(encrypted_data[:, :8]).astype(np.uint8),
        bits_to_int(encrypted_data[:, 8:16]).astype(np.uint8),
        bits_to_int(encrypted_data[:, 16:24]).astype(np.uint8),
        bits_to_int(encrypted_data[:, 24:]).astype(np.uint8)
    )

    encrypted_image = list(zip(*rgba_values))

    with Image.open(input_path) as image:
        image.putdata(encrypted_image)
        image.save(output_path)
