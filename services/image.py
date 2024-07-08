import numpy as np
import numpy.typing as npt
from PIL import Image


PIXEL_SIZE_BITS = 32
NUM_VALUES_PER_PIXEL = 4


def integer_array_to_binary_array(integer_array: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
    return ((np.reshape(integer_array, (-1, 1)) & (1 << np.arange(8, dtype=np.uint8))) != 0).astype(np.uint8)[:, ::-1]


def binary_array_to_integer_array(binary_array: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
    return (binary_array * (1 << np.arange(8)[::-1])).sum(axis=1)


def get_pixels(input_path: str):
    with Image.open(input_path) as image:
        data = np.array(image.getdata(), dtype=np.uint8)
        data_bits = integer_array_to_binary_array(data).reshape(-1)
        
    return data_bits


def put_pixels(input_path: str, output_path: str, encrypted_data):
    encrypted_data = encrypted_data.reshape(-1, PIXEL_SIZE_BITS)

    rgba_values = (
        binary_array_to_integer_array(encrypted_data[:, :8]).astype(np.uint8),
        binary_array_to_integer_array(encrypted_data[:, 8:16]).astype(np.uint8),
        binary_array_to_integer_array(encrypted_data[:, 16:24]).astype(np.uint8),
        binary_array_to_integer_array(encrypted_data[:, 24:]).astype(np.uint8)
    )

    encrypted_image = list(zip(*rgba_values))

    with Image.open(input_path) as image:
        image.putdata(encrypted_image)
        image.save(output_path)