import numpy as np
from Crypto.Cipher import DES
from PIL import Image
import itertools
import multiprocessing

# ✅ Convert integer key to DES key format (8 bytes)
def int_to_key(n):
    return n.to_bytes(8, 'big')

# ✅ Decrypt DES-encrypted image pixels using a given key
def decrypt_image_pixels(encrypted_pixels, key):
    cipher = DES.new(key, DES.MODE_ECB)
    return cipher.decrypt(encrypted_pixels)

# ✅ Check if the decrypted pixels contain a recognizable pattern
def is_valid_image(decrypted_pixels):
    return decrypted_pixels[:2] == b'\xFF\xD8'  # Example: JPEG header

# ✅ Brute-force attack function
def brute_force_attack(encrypted_pixels, start_key=0, end_key=2**56):
    for key_int in range(start_key, end_key):
        key = int_to_key(key_int)
        decrypted_pixels = decrypt_image_pixels(encrypted_pixels, key)

        if is_valid_image(decrypted_pixels):
            print(f"🔑 Key found: {hex(key_int)}")
            return key_int

    return None

# ✅ Multiprocessing Wrapper for Faster Cracking
def parallel_brute_force(encrypted_pixels, num_workers=4):
    key_space = 2**56
    chunk_size = key_space // num_workers

    with multiprocessing.Pool(num_workers) as pool:
        results = pool.starmap(brute_force_attack, 
                               [(encrypted_pixels, i * chunk_size, (i + 1) * chunk_size) 
                                for i in range(num_workers)])
    
    return next((key for key in results if key is not None), None)

# ✅ Load Encrypted Image
def load_encrypted_image(image_path):
    img = Image.open(image_path)
    img = img.convert("L")  # Convert to grayscale
    pixels = np.array(img).tobytes()
    return img.size, pixels

# ✅ Save the decrypted image
def save_decrypted_image(decrypted_pixels, image_size, output_path="decrypted_image.png"):
    decrypted_array = np.frombuffer(decrypted_pixels, dtype=np.uint8).reshape(image_size)
    decrypted_img = Image.fromarray(decrypted_array, mode="L")
    decrypted_img.save(output_path)
    print(f"✅ Decrypted image saved as {output_path}")

# ✅ Main Function
if __name__ == "__main__":
    image_path = "/mnt/c/Users/wadoud/Downloads/Security/des-image-encryption/lena_grayscale-ECB_ENCRYPTION.png"  # Replace with actual encrypted image path
    image_size, encrypted_pixels = load_encrypted_image(image_path)

    print("🚀 Starting Brute-Force Attack...")
    found_key = parallel_brute_force(encrypted_pixels, num_workers=8)

    if found_key is not None:
        print(f"🎉 Successfully cracked DES! Key: {hex(found_key)}")
        key = int_to_key(found_key)
        decrypted_pixels = decrypt_image_pixels(encrypted_pixels, key)
        save_decrypted_image(decrypted_pixels, image_size)
    else:
        print("❌ Failed to find the key.")
