import numpy as np
import numpy.typing as npt
from PIL import Image


def integer_array_to_binary_array(integer_array: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
    """Convert integer array (0-255) to binary array (8 bits per integer)."""
    return ((np.reshape(integer_array, (-1, 1)) & (1 << np.arange(8, dtype=np.uint8))) != 0).astype(np.uint8)[:, ::-1]


def binary_array_to_integer_array(binary_array: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
    """Convert binary array (each 8 bits) back to integer array (0-255)."""
    return (binary_array * (1 << np.arange(8)[::-1])).sum(axis=1).astype(np.uint8)


def get_pixels(input_path: str) -> npt.NDArray[np.uint8]:
    with Image.open(input_path) as image:
        if image.mode == "L":
            data = np.array(image.getdata(), dtype=np.uint8)
            binary_data = integer_array_to_binary_array(data)
            return binary_data.reshape(-1)
        elif image.mode in ("RGB", "RGBA"):
            data = np.array(image.getdata(), dtype=np.uint8)
            binary_data = integer_array_to_binary_array(data)
            return binary_data.reshape(-1)
        else:
            raise ValueError(f"Image mode {image.mode} not supported.")


def put_pixels(input_path: str, output_path: str, encrypted_data: npt.NDArray[np.uint8]):
    with Image.open(input_path) as image:
        if image.mode == "L":
            # Grayscale images - 1 byte (8 bits) per pixel
            encrypted_data = encrypted_data.reshape(-1, 8)
            pixel_values = binary_array_to_integer_array(encrypted_data)
            encrypted_image = Image.new("L", image.size)
            encrypted_image.putdata(pixel_values)
            encrypted_image.save(output_path)

        elif image.mode == "RGB":
            # RGB images - 3 bytes (24 bits) per pixel
            encrypted_data = encrypted_data.reshape(-1, 24)
            pixel_values = (
                binary_array_to_integer_array(encrypted_data[:, :8]),
                binary_array_to_integer_array(encrypted_data[:, 8:16]),
                binary_array_to_integer_array(encrypted_data[:, 16:24]),
            )
            encrypted_image = Image.new("RGB", image.size)
            encrypted_image.putdata(list(zip(*pixel_values)))
            encrypted_image.save(output_path)

        elif image.mode == "RGBA":
            # RGBA images - 4 bytes (32 bits) per pixel
            encrypted_data = encrypted_data.reshape(-1, 32)
            pixel_values = (
                binary_array_to_integer_array(encrypted_data[:, :8]),
                binary_array_to_integer_array(encrypted_data[:, 8:16]),
                binary_array_to_integer_array(encrypted_data[:, 16:24]),
                binary_array_to_integer_array(encrypted_data[:, 24:]),
            )
            encrypted_image = Image.new("RGBA", image.size)
            encrypted_image.putdata(list(zip(*pixel_values)))
            encrypted_image.save(output_path)

        else:
            raise ValueError(f"Image mode {image.mode} not supported.")