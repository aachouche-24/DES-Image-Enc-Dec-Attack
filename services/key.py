import data.constants as constants
import numpy as np
import numpy.typing as npt
import secrets
from services.des import permute


def generate_key(integer = secrets.randbits(64)) -> npt.NDArray[np.uint8]:
    binary_strings = list(format(integer, "b"))
    array = np.array(binary_strings, dtype=np.uint8)
    padding = 64 - len(binary_strings)
    
    return np.pad(array, (padding, 0))


def generate_subkeys(key: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
    permuted_key = permute(constants.PC_1, key)

    c = permuted_key[:28]
    d = permuted_key[28:]

    subkeys = np.empty((16, 48), dtype=np.uint8)

    for i, shift in enumerate(constants.SHIFTS):
        c = np.roll(c, shift * -1)
        d = np.roll(d, shift * -1)

        cd_combined = np.hstack((c, d))

        subkey = permute(constants.PC_2, cd_combined)
        subkeys[i] = subkey

    return subkeys