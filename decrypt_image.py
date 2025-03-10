import argparse
import os
from PIL import Image
import services.key as Key
import services.mode as Mode
from services.image import get_pixels, put_pixels


def main():
    parser = argparse.ArgumentParser(
        description="A Python-based image decryption application that enables users to decrypt image files using the Data Encryption Standard (DES) algorithm. This tool supports five different decryption modes: ECB, CBC, CFB, OFB, and CTR.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Set defaults to make testing easier
    parser.add_argument("input", type=str, nargs='?', default="Black_square-ECB_ENCRYPTION.png", help="The relative path to the encrypted image file you wish to decrypt.")
    parser.add_argument("mode", type=str, nargs='?', choices=["ECB", "CBC", "CFB", "OFB", "CTR"], default="ECB", help="The decryption mode to use.")
    parser.add_argument("key", type=str, nargs='?', default="0x133457799bbcdff1", help="A 64-bit integer representing the key to decrypt the image with, in hexadecimal.")

    args = parser.parse_args()

    # Convert key to integer if it's passed as a hexadecimal string
    if args.key.startswith('0x'):
        args.key = int(args.key, 16)

    print(f"🔑 Decryption key: {hex(args.key)}")

    # Check if the image is in RGB, RGBA, or grayscale
    with Image.open(args.input) as img:
        if img.mode == 'RGB':
            print(f"🔵 Image is in RGB mode. Proceeding with RGB decryption.")
        elif img.mode == 'RGBA':
            print(f"🖼️ Image is in RGBA mode. Proceeding with RGBA decryption.")
        elif img.mode == 'L':
            print(f"⚪ Image is in Grayscale (L) mode. Proceeding with grayscale decryption.")
        else:
            print(f"❌ Your input image is not supported. The image mode is '{img.mode}'. Please provide an RGB, RGBA, or Grayscale image.")
            return  # Exit if the image is not RGB, RGBA, or grayscale

    try:
        pixels = get_pixels(args.input)
    except ValueError as e:
        raise ValueError(f"Failed to read image pixels: {e}")

    # Convert key from integer to bit array
    key = Key.generate_key(args.key)
    subkeys = Key.generate_subkeys(key)

    # Perform DES decryption based on the mode selected
    match args.mode:
        case "ECB":
            decrypted_data = Mode.ecb(pixels, subkeys, decrypt=True)
        case "CBC":
            decrypted_data = Mode.cbc(pixels, subkeys, decrypt=True)
        case "CFB":
            decrypted_data = Mode.cfb(pixels, subkeys, decrypt=True)
        case "OFB":
            decrypted_data = Mode.ofb(pixels, subkeys, decrypt=True)
        case "CTR":
            decrypted_data = Mode.ctr(pixels, subkeys, decrypt=True)

    # Save the decrypted image
    output_file = f"decrypted_{args.mode}_{os.path.basename(args.input)}"
    put_pixels(args.input, output_file, decrypted_data)
    print(f"✅ Image decrypted and saved to {output_file}.")
    print(f"🔑 Decryption key: {hex(args.key)}")


if __name__ == "__main__":
    main()
