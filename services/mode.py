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


def ecb(text: npt.NDArray[np.uint8], subkeys: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
    num_blocks = len(text) // BLOCK_SIZE_BITS
    encryption = np.empty(num_blocks * BLOCK_SIZE_BITS, dtype=np.uint8)

    for i in tqdm(
        range(num_blocks),
        desc="Encryption in ECB Mode",
        total=num_blocks
    ):
        start = i * BLOCK_SIZE_BITS
        end = start + BLOCK_SIZE_BITS
        encrypted_block = encrypt(text[start:end], subkeys)
        encryption[start:end] = encrypted_block

    return encryption


def cbc(text: npt.NDArray[np.uint8], subkeys: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
    # TODO: create a more robust IV
    IV = np.zeros(BLOCK_SIZE_BITS, dtype=np.uint8)

    num_blocks = len(text) // BLOCK_SIZE_BITS
    encryption = np.empty(num_blocks * BLOCK_SIZE_BITS, dtype=np.uint8)

    for i in tqdm(
        range(num_blocks),
        desc="Encryption in CBC Mode",
        total=num_blocks
    ):
        start = i * BLOCK_SIZE_BITS
        end = start + BLOCK_SIZE_BITS

        block = np.bitwise_xor(text[start:end], IV)
        encrypted_block = encrypt(block, subkeys)
        IV = encrypted_block
        encryption[start:end] = encrypted_block

    return encryption


def cfb(text: npt.NDArray[np.uint8], subkeys: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
    shift_register = np.zeros(BLOCK_SIZE_BITS, dtype=np.uint8)

    num_segments = len(text) // SEGMENT_SIZE_BITS
    ciphertext = np.empty(num_segments * SEGMENT_SIZE_BITS, dtype=np.uint8)

    for i in tqdm(
        range(num_segments),
        desc="Encryption in CFB Mode",
        total=num_segments
    ):
        start = i * SEGMENT_SIZE_BITS
        end = start + SEGMENT_SIZE_BITS

        encryption = encrypt(shift_register, subkeys)
        plaintext_segment = text[start:end]
        
        ciphertext_segment = np.bitwise_xor(encryption[:SEGMENT_SIZE_BITS], plaintext_segment)
        ciphertext[start:end] = ciphertext_segment

        shift_register = np.roll(shift_register, -1 * SEGMENT_SIZE_BITS)
        shift_register[-1 * SEGMENT_SIZE_BITS:] = ciphertext_segment

    return ciphertext


def ofb(text: npt.NDArray[np.uint8], subkeys: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
    # TODO: create a more robust nonce
    nonce = np.zeros(BLOCK_SIZE_BITS, dtype=np.uint8)
    
    num_blocks = len(text) // BLOCK_SIZE_BITS
    plaintext = np.empty(num_blocks * BLOCK_SIZE_BITS, dtype=np.uint8)

    for i in tqdm(
        range(num_blocks),
        desc="Encryption in OFB Mode",
        total=num_blocks
    ):
        start = i * BLOCK_SIZE_BITS
        end = start + BLOCK_SIZE_BITS

        nonce = encrypt(nonce, subkeys)
        plaintext_block = text[start:end]
        ciphertext_block = np.bitwise_xor(plaintext_block, nonce[:len(plaintext_block)])
        plaintext[start:end] = ciphertext_block

    return plaintext


def ctr(text: npt.NDArray[np.uint8], subkeys: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
    num_blocks = len(text) // BLOCK_SIZE_BITS
    ciphertext = np.empty(num_blocks * BLOCK_SIZE_BITS, dtype=np.uint8)
    counter = 0
    bit_size = 64

    for i in tqdm(
        range(num_blocks),
        desc="Encryption in CTR Mode",
        total=num_blocks
    ):
        counter_block = np.array([(counter >> bit) & 1 for bit in range(bit_size - 1, -1, -1)], dtype=np.uint8)

        encryption = encrypt(counter_block, subkeys)
        start = i * BLOCK_SIZE_BITS
        end = start + BLOCK_SIZE_BITS
        plaintext_block = text[start:end]
        ciphertext_block = np.bitwise_xor(plaintext_block, encryption[:len(plaintext_block)])
        ciphertext[start:end] = ciphertext_block

        counter = (counter + 1) % (2 ** bit_size)

    return ciphertext