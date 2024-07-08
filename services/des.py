import data.constants as constants
import numpy as np
import numpy.typing as npt


def permute(permutation_table, bit_string):
    return bit_string[permutation_table - 1]


def encrypt(text, subkeys: npt.NDArray[np.uint8]):
    permuted_message = permute(constants.IP, text)
    l = permuted_message[:32]
    r = permuted_message[32:]

    for subkey in subkeys:
        xor = subkey ^ permute(constants.E_BIT, r)
        result = np.empty((0,), dtype=np.uint8)

        for i in range(8):
            six_bits = xor[i * 6 : (i + 1) * 6]
            row = (six_bits[0] << 1) + six_bits[5]
            col = (six_bits[1] << 3) + (six_bits[2] << 2) + (six_bits[3] << 1) + six_bits[4]

            s_box_value = constants.S_BOXES[i][row][col]
            result = np.concatenate((result, constants.S_BOX_CONVERSION[s_box_value]))

        f = permute(constants.P, result)
        l, r = r, l ^ f

    return permute(constants.IP_I, np.concatenate((r, l)))