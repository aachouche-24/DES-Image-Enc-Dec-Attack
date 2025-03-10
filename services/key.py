import data.constants as constants
import numpy as np
import numpy.typing as npt


def generate_key(integer: int) -> npt.NDArray[np.uint8]:
    """Convert an integer into a 64-bit binary array."""
    # Convert the integer to a 64-bit binary string, pad with zeros if necessary
    binary_string = f"{integer:064b}"
    
    # Convert the binary string into a NumPy array of uint8 (0 or 1)
    array = np.array([int(bit) for bit in binary_string], dtype=np.uint8)
    
    return array


def generate_subkeys(key: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
    """Generate 16 subkeys from the 64-bit key."""
    # Perform the PC-1 permutation on the key
    permuted_key = key[constants.PC_1 - 1]

    # Split the permuted key into left and right halves (28 bits each)
    c = permuted_key[:28]
    d = permuted_key[28:]

    subkeys = np.empty((16, 48), dtype=np.uint8)

    # Generate the 16 subkeys using the key schedule
    for i, shift in enumerate(constants.SHIFTS):
        # Perform circular shifts on both halves (c and d)
        c = np.roll(c, shift * -1)  # Negative shift to rotate left
        d = np.roll(d, shift * -1)  # Negative shift to rotate left

        # Combine the two halves (c and d)
        cd_combined = np.hstack((c, d))

        # Apply the PC-2 permutation to the combined key
        subkey = cd_combined[constants.PC_2 - 1]
        subkeys[i] = subkey

    return subkeys
