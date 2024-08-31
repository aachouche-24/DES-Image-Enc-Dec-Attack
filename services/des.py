import data.constants as constants
import numpy as np
import numpy.typing as npt


def encrypt(text, subkeys: npt.NDArray[np.uint8]):
    permutation = text[constants.IP - 1]
    l = permutation[:32]
    r = permutation[32:]

    for subkey in subkeys:
        xor = subkey ^ r[constants.E_BIT - 1]
        result = np.empty((0,), dtype=np.uint8)

        for i in range(8):
            six_bits = xor[i * 6 : (i + 1) * 6]
            row = (six_bits[0] << 1) + six_bits[5]
            col = (six_bits[1] << 3) + (six_bits[2] << 2) + (six_bits[3] << 1) + six_bits[4]

            s_box_value = constants.S_BOXES[i][row][col]
            result = np.concatenate((result, constants.S_BOX_CONVERSION[s_box_value]))

        f = result[constants.P - 1]
        l, r = r, l ^ f

    return np.concatenate((r, l))[constants.IP_I - 1]