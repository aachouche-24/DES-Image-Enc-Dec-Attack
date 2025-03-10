import numpy as np
import numpy.typing as npt
from services.des import encrypt
from tqdm import tqdm


BLOCK_SIZE_BITS = 64
SEGMENT_SIZE_BITS = 8


def pad_text(text: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
    padding = np.zeros(BLOCK_SIZE_BITS - (len(text) % BLOCK_SIZE_BITS), dtype=np.uint8)
    return np.concatenate((text, padding), dtype=np.uint8)


def unpad_text(text: npt.NDArray[np.uint8], padding_length: int) -> npt.NDArray[np.uint8]:
    return text[:len(text) - padding_length]


def ecb(text: npt.NDArray[np.uint8], subkeys: npt.NDArray[np.uint8], decrypt=False) -> npt.NDArray[np.uint8]:
    num_blocks = len(text) // BLOCK_SIZE_BITS
    result = np.empty(num_blocks * BLOCK_SIZE_BITS, dtype=np.uint8)

    for i in tqdm(
        range(num_blocks),
        desc="Processing in ECB Mode",
        total=num_blocks
    ):
        start = i * BLOCK_SIZE_BITS
        end = start + BLOCK_SIZE_BITS
        if decrypt:
            # For decryption, we just call encrypt with decrypt=True
            result[start:end] = encrypt(text[start:end], subkeys, decrypt=True)
        else:
            result[start:end] = encrypt(text[start:end], subkeys)

    return result


def cbc(text: npt.NDArray[np.uint8], subkeys: npt.NDArray[np.uint8], decrypt=False) -> npt.NDArray[np.uint8]:
    IV = np.zeros(BLOCK_SIZE_BITS, dtype=np.uint8)  # Initialization Vector (can be more complex)

    num_blocks = len(text) // BLOCK_SIZE_BITS
    result = np.empty(num_blocks * BLOCK_SIZE_BITS, dtype=np.uint8)

    for i in tqdm(
        range(num_blocks),
        desc="Processing in CBC Mode",
        total=num_blocks
    ):
        start = i * BLOCK_SIZE_BITS
        end = start + BLOCK_SIZE_BITS

        if decrypt:
            # Decryption: Reverse the XOR and encryption sequence
            decrypted_block = encrypt(text[start:end], subkeys, decrypt=True)
            result[start:end] = np.bitwise_xor(decrypted_block, IV)
            IV = text[start:end]  # Update IV with the previous block
        else:
            # Encryption: XOR with IV before encrypting
            block = np.bitwise_xor(text[start:end], IV)
            encrypted_block = encrypt(block, subkeys)
            IV = encrypted_block  # Update IV with the encrypted block
            result[start:end] = encrypted_block

    return result


def cfb(text: npt.NDArray[np.uint8], subkeys: npt.NDArray[np.uint8], decrypt=False) -> npt.NDArray[np.uint8]:
    shift_register = np.zeros(BLOCK_SIZE_BITS, dtype=np.uint8)

    num_segments = len(text) // SEGMENT_SIZE_BITS
    result = np.empty(num_segments * SEGMENT_SIZE_BITS, dtype=np.uint8)

    for i in tqdm(
        range(num_segments),
        desc="Processing in CFB Mode",
        total=num_segments
    ):
        start = i * SEGMENT_SIZE_BITS
        end = start + SEGMENT_SIZE_BITS

        if decrypt:
            # Decryption: Use the encryption output to XOR with the ciphertext
            encryption = encrypt(shift_register, subkeys, decrypt=True)
            result_segment = np.bitwise_xor(encryption[:SEGMENT_SIZE_BITS], text[start:end])
        else:
            # Encryption: Perform normal encryption and shift register updates
            encryption = encrypt(shift_register, subkeys)
            result_segment = np.bitwise_xor(encryption[:SEGMENT_SIZE_BITS], text[start:end])

        result[start:end] = result_segment
        shift_register = np.roll(shift_register, -1 * SEGMENT_SIZE_BITS)
        shift_register[-1 * SEGMENT_SIZE_BITS:] = result_segment

    return result


def ofb(text: npt.NDArray[np.uint8], subkeys: npt.NDArray[np.uint8], decrypt=False) -> npt.NDArray[np.uint8]:
    nonce = np.zeros(BLOCK_SIZE_BITS, dtype=np.uint8)

    num_blocks = len(text) // BLOCK_SIZE_BITS
    result = np.empty(num_blocks * BLOCK_SIZE_BITS, dtype=np.uint8)

    for i in tqdm(
        range(num_blocks),
        desc="Processing in OFB Mode",
        total=num_blocks
    ):
        start = i * BLOCK_SIZE_BITS
        end = start + BLOCK_SIZE_BITS

        # OFB mode encryption and decryption are identical, since it's just XOR with nonce
        nonce = encrypt(nonce, subkeys, decrypt=True) if decrypt else encrypt(nonce, subkeys)
        result[start:end] = np.bitwise_xor(text[start:end], nonce[:len(text[start:end])])

    return result


def ctr(text: npt.NDArray[np.uint8], subkeys: npt.NDArray[np.uint8], decrypt=False) -> npt.NDArray[np.uint8]:
    num_blocks = len(text) // BLOCK_SIZE_BITS
    result = np.empty(num_blocks * BLOCK_SIZE_BITS, dtype=np.uint8)
    counter = 0
    bit_size = 64

    for i in tqdm(
        range(num_blocks),
        desc="Processing in CTR Mode",
        total=num_blocks
    ):
        counter_block = np.array([(counter >> bit) & 1 for bit in range(bit_size - 1, -1, -1)], dtype=np.uint8)

        encryption = encrypt(counter_block, subkeys, decrypt=True) if decrypt else encrypt(counter_block, subkeys)
        start = i * BLOCK_SIZE_BITS
        end = start + BLOCK_SIZE_BITS
        result[start:end] = np.bitwise_xor(text[start:end], encryption[:len(text[start:end])])

        counter = (counter + 1) % (2 ** bit_size)

    return result
